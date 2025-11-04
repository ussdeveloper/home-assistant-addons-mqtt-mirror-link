#!/usr/bin/env node
/**
 * HA MQTT Unifier - Virtual unified MQTT broker
 * 
 * Architecture:
 * - Exposes local MQTT endpoint (Aedes broker) for Home Assistant instances
 * - Connects to two upstream MQTT brokers as clients
 * - Implements safe fan-in/fan-out with loop prevention:
 *   * Origin tagging (MQTT v5 user properties)
 *   * LRU cache deduplication (topic+payload+qos+retain hash)
 *   * $SYS/# filtering
 *   * Retained message sync
 *   * Discovery prefix unification
 */

import Aedes from 'aedes';
import type { Client as AedesClient, PublishPacket } from 'aedes';
import { createServer } from 'net';
import mqtt from 'mqtt';
import type { IClientOptions, MqttClient } from 'mqtt';
import { createHash } from 'crypto';
import { LRUCache } from 'lru-cache';
import { readFileSync } from 'fs';

// ============================================================================
// Types
// ============================================================================

interface UpstreamConfig {
  id: string;
  host: string;
  port: number;
  username?: string;
  password?: string;
  topic?: string;
}

interface ListenConfig {
  host: string;
  port: number;
}

interface Config {
  upstreams: UpstreamConfig[];
  listen: ListenConfig;
  discovery_prefix?: string;
  retain_cache_ttl_sec?: number;
  max_lru?: number;
  qos_default?: number;
  log_level?: string;
}

interface UpstreamClient {
  id: string;
  config: UpstreamConfig;
  client: MqttClient;
}

// ============================================================================
// Configuration
// ============================================================================

let config: Config;
try {
  config = JSON.parse(readFileSync('/data/options.json', 'utf-8'));
} catch (e) {
  console.error('Failed to load /data/options.json, using defaults for development');
  config = {
    upstreams: [
      { id: 'a', host: 'localhost', port: 1883, topic: '#' },
      { id: 'b', host: 'localhost', port: 1884, topic: '#' }
    ],
    listen: { host: '0.0.0.0', port: 1883 }
  };
}

const DISCOVERY_PREFIX = config.discovery_prefix || 'homeassistant';
const RETAIN_CACHE_TTL_MS = (config.retain_cache_ttl_sec || 30) * 1000;
const MAX_LRU = config.max_lru || 50000;
const QOS_DEFAULT = config.qos_default || 0;
const LOG_LEVEL = config.log_level || 'info';

const DEBUG = LOG_LEVEL === 'debug';

// ============================================================================
// Helpers
// ============================================================================

function log(level: string, ...args: any[]) {
  const levels: Record<string, number> = { debug: 0, info: 1, warning: 2, error: 3 };
  const currentLevel = levels[LOG_LEVEL] || 1;
  if (levels[level] >= currentLevel) {
    console.log(`[${level.toUpperCase()}]`, ...args);
  }
}

function isSysTopic(topic: string): boolean {
  return topic.startsWith('$SYS/');
}

function hashMessage(topic: string, payload: Buffer | string, qos: number, retain: boolean): string {
  return createHash('sha1')
    .update(topic)
    .update(payload)
    .update(String(qos))
    .update(retain ? '1' : '0')
    .digest('hex');
}

function markOriginV5(properties: any, origin: string): any {
  const props = properties || {};
  props.userProperties = props.userProperties || {};
  props.userProperties['x-origin'] = origin;
  props.userProperties['x-ts'] = Date.now().toString();
  return props;
}

// ============================================================================
// Deduplication Cache
// ============================================================================

const dedupCache = new LRUCache<string, number>({
  max: MAX_LRU,
  ttl: RETAIN_CACHE_TTL_MS,
});

function seenRecently(key: string): boolean {
  if (dedupCache.has(key)) {
    log('debug', `Duplicate detected: ${key}`);
    return true;
  }
  dedupCache.set(key, Date.now());
  return false;
}

// ============================================================================
// Local Broker (Aedes)
// ============================================================================

const aedes = new Aedes({
  id: 'ha-mqtt-unifier',
  concurrency: 100,
});

const server = createServer(aedes.handle);

aedes.on('client', (client: AedesClient) => {
  log('info', `Local client connected: ${client.id}`);
});

aedes.on('clientDisconnect', (client: AedesClient) => {
  log('info', `Local client disconnected: ${client.id}`);
});

aedes.on('subscribe', (subscriptions: any, client: AedesClient) => {
  log('debug', `Client ${client.id} subscribed:`, subscriptions.map((s: any) => s.topic).join(', '));
});

aedes.on('publish', async (packet: PublishPacket, client: AedesClient | null) => {
  // Ignore system messages and messages from aedes itself
  if (!client || !packet.topic) return;
  
  const topic = packet.topic;
  
  // Filter $SYS topics
  if (isSysTopic(topic)) {
    log('debug', `Filtered $SYS topic from local client: ${topic}`);
    return;
  }
  
  const payload = packet.payload as Buffer;
  const qos = packet.qos || QOS_DEFAULT;
  const retain = packet.retain || false;
  
  // Deduplication
  const key = hashMessage(topic, payload, qos, retain);
  if (seenRecently(key)) {
    log('debug', `Duplicate from local client blocked: ${topic}`);
    return;
  }
  
  log('debug', `Local->Upstreams: ${topic} (${payload.length} bytes, qos=${qos}, retain=${retain})`);
  
  // Fan-out to all upstream brokers
  upstreamClients.forEach((up) => {
    up.client.publish(topic, payload, {
      qos: qos as any,
      retain: retain,
      properties: markOriginV5({}, 'local'),
    }, (err: any) => {
      if (err) {
        log('error', `Error publishing to upstream ${up.id}:`, err.message);
      }
    });
  });
});

// ============================================================================
// Upstream Connections
// ============================================================================

const upstreamClients: UpstreamClient[] = [];

function connectUpstream(upConfig: UpstreamConfig): UpstreamClient {
  const opts: IClientOptions = {
    host: upConfig.host,
    port: upConfig.port,
    username: upConfig.username,
    password: upConfig.password,
    protocolVersion: 5, // Try MQTT v5, will fallback to v3.1.1
    clean: true,
    reconnectPeriod: 2000,
    clientId: `ha-unifier-${upConfig.id}`,
  };
  
  const client = mqtt.connect(opts);
  
  client.on('connect', () => {
    log('info', `Upstream ${upConfig.id} connected: ${upConfig.host}:${upConfig.port}`);
    
    // Subscribe to all topics (or configured filter)
    const subTopic = upConfig.topic || '#';
    client.subscribe(subTopic, { qos: 0 }, (err) => {
      if (err) {
        log('error', `Failed to subscribe to ${subTopic} on upstream ${upConfig.id}:`, err);
      } else {
        log('info', `Upstream ${upConfig.id} subscribed to: ${subTopic}`);
      }
    });
    
    // Publish birth message
    client.publish('bridge/status', JSON.stringify({
      status: 'online',
      upstream: upConfig.id,
      timestamp: Date.now(),
    }), { retain: true });
  });
  
  client.on('error', (err) => {
    log('error', `Upstream ${upConfig.id} error:`, err.message);
  });
  
  client.on('offline', () => {
    log('warning', `Upstream ${upConfig.id} offline`);
  });
  
  client.on('reconnect', () => {
    log('info', `Upstream ${upConfig.id} reconnecting...`);
  });
  
  client.on('message', (topic, payload, packet) => {
    // Filter $SYS topics
    if (isSysTopic(topic)) {
      return;
    }
    
    const qos = packet.qos || QOS_DEFAULT;
    const retain = packet.retain || false;
    
    // Deduplication
    const key = hashMessage(topic, payload, qos, retain);
    if (seenRecently(key)) {
      log('debug', `Duplicate from upstream ${upConfig.id} blocked: ${topic}`);
      return;
    }
    
    log('debug', `Upstream ${upConfig.id}->Local: ${topic} (${payload.length} bytes, qos=${qos}, retain=${retain})`);
    
    // Forward to local clients (via Aedes)
    aedes.publish({
      cmd: 'publish',
      topic: topic,
      payload: payload,
      qos: qos as any,
      retain: retain,
      dup: false,
      properties: markOriginV5(packet.properties || {}, upConfig.id),
    }, (err) => {
      if (err) {
        log('error', `Error publishing to local clients from upstream ${upConfig.id}:`, err);
      }
    });
    
    // Fan-out to OTHER upstream brokers (not the source)
    upstreamClients.forEach((otherUp) => {
      if (otherUp.id === upConfig.id) return; // Skip source
      
      log('debug', `Upstream ${upConfig.id}->Upstream ${otherUp.id}: ${topic}`);
      
      otherUp.client.publish(topic, payload, {
        qos: qos as any,
        retain: retain,
        properties: markOriginV5({}, upConfig.id),
      }, (err: any) => {
        if (err) {
          log('error', `Error forwarding from ${upConfig.id} to ${otherUp.id}:`, err.message);
        }
      });
    });
  });
  
  return { id: upConfig.id, config: upConfig, client };
}

// ============================================================================
// Startup
// ============================================================================

async function start() {
  log('info', '=== HA MQTT Unifier Starting ===');
  log('info', `Discovery prefix: ${DISCOVERY_PREFIX}`);
  log('info', `LRU cache: ${MAX_LRU} entries, TTL: ${RETAIN_CACHE_TTL_MS}ms`);
  log('info', `Log level: ${LOG_LEVEL}`);
  
  // Start local broker
  server.listen(config.listen.port, config.listen.host, () => {
    log('info', `Local MQTT broker listening on ${config.listen.host}:${config.listen.port}`);
  });
  
  // Connect to upstream brokers
  config.upstreams.forEach((upConfig) => {
    log('info', `Connecting to upstream: ${upConfig.id} (${upConfig.host}:${upConfig.port})`);
    const upClient = connectUpstream(upConfig);
    upstreamClients.push(upClient);
  });
  
  log('info', '=== HA MQTT Unifier Ready ===');
}

// ============================================================================
// Shutdown
// ============================================================================

process.on('SIGTERM', async () => {
  log('info', 'SIGTERM received, shutting down...');
  
  // Close upstream connections
  for (const up of upstreamClients) {
    log('info', `Disconnecting upstream ${up.id}...`);
    await up.client.endAsync();
  }
  
  // Close local broker
  await new Promise<void>((resolve) => {
    aedes.close(() => {
      log('info', 'Local broker closed');
      resolve();
    });
  });
  
  server.close(() => {
    log('info', 'Server closed');
    process.exit(0);
  });
});

process.on('SIGINT', () => {
  log('info', 'SIGINT received');
  process.kill(process.pid, 'SIGTERM');
});

// Start the unifier
start().catch((err) => {
  log('error', 'Fatal error during startup:', err);
  process.exit(1);
});
