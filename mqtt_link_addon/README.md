# MQTT Unified Broker - Add-on for Home Assistant

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)

Virtual unified MQTT broker that exposes a single local endpoint for multiple Home Assistant instances while safely bridging multiple upstream MQTT brokers.

## Architecture Overview

**Problem:** When linking two Home Assistant instances with separate MQTT brokers, traditional bridging creates message loops and duplicate messages.

**Solution:** This add-on creates a **virtual unified broker** that:
- Exposes a single MQTT endpoint (e.g., `localhost:1883`) for your Home Assistant instances
- Connects to multiple upstream MQTT brokers as a client
- Implements intelligent message routing with:
  - **LRU cache deduplication** - prevents message loops
  - **Origin tagging** - tracks message source using MQTT v5 user properties
  - **$SYS filtering** - blocks system topics from forwarding
  - **Retained message sync** - smart cache of retained messages
  - **Discovery prefix unification** - single `homeassistant/` namespace

## How It Works

```
┌─────────────────┐         ┌─────────────────┐
│ Home Assistant  │         │ Home Assistant  │
│   Instance A    │         │   Instance B    │
└────────┬────────┘         └────────┬────────┘
         │                           │
         └───────────┬───────────────┘
                     │
           ┌─────────▼─────────┐
           │  Unified Broker   │  ← This Add-on
           │  (localhost:1883) │     (Aedes + mqtt.js)
           └─────────┬─────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
    ┌────▼────┐            ┌────▼────┐
    │ MQTT    │            │ MQTT    │
    │Upstream │            │Upstream │
    │   A     │            │   B     │
    └─────────┘            └─────────┘
```

### Message Flow

1. **Local Publish** (from HA): Message published to unified broker → forwarded to ALL upstreams
2. **Upstream Publish**: Message received from upstream A → forwarded to local clients AND upstream B (not back to A)
3. **Deduplication**: Each message hashed (`sha1(topic+payload+qos+retain)`) with TTL cache - duplicates blocked in <1ms
4. **No Loops**: Origin tracking prevents ping-pong between upstreams

## Features

✅ **Zero-loop architecture** - intelligent deduplication prevents infinite message loops  
✅ **MQTT v5 ready** - uses user properties for origin tagging, falls back to v3.1.1  
✅ **QoS & Retain preservation** - maintains message properties across brokers  
✅ **Discovery unification** - single `homeassistant/` prefix for all devices  
✅ **Multi-upstream** - supports 2+ upstream brokers  
✅ **Configurable caching** - LRU cache with adjustable size and TTL  
✅ **Debug logging** - detailed message flow tracing  

## Installation

### Add Repository

1. In Home Assistant, go to **Settings** → **Add-ons**
2. Click **Add-on Store** (bottom right)
3. Click **⋮** menu → **Repositories**
4. Add: `https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link`
5. Find **MQTT Unified Broker** and click **Install**

## Configuration

### Basic Example

```yaml
upstreams:
  - id: "upstream_a"
    host: "192.168.1.10"
    port: 1883
    username: "mqtt_user"
    password: "secret123"
    topic: "#"
  - id: "upstream_b"
    host: "192.168.1.11"
    port: 1883
    username: "mqtt_user"
    password: "secret456"
    topic: "#"
listen:
  host: "0.0.0.0"
  port: 1883
discovery_prefix: "homeassistant"
retain_cache_ttl_sec: 30
max_lru: 50000
qos_default: 0
log_level: "info"
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `upstreams` | list | required | List of upstream MQTT brokers to bridge |
| `upstreams[].id` | string | required | Unique identifier for this upstream |
| `upstreams[].host` | string | required | Hostname or IP address |
| `upstreams[].port` | int | 1883 | MQTT port |
| `upstreams[].username` | string | optional | MQTT username |
| `upstreams[].password` | string | optional | MQTT password |
| `upstreams[].topic` | string | `#` | Topic filter to subscribe |
| `listen.host` | string | `0.0.0.0` | Local bind address |
| `listen.port` | int | 1883 | Local MQTT port |
| `discovery_prefix` | string | `homeassistant` | HA discovery prefix |
| `retain_cache_ttl_sec` | int | 30 | Cache TTL in seconds (10-300) |
| `max_lru` | int | 50000 | Max LRU cache entries (1000-100000) |
| `qos_default` | int | 0 | Default QoS level (0-2) |
| `log_level` | string | `info` | `debug`, `info`, `warning`, `error` |

## Usage

### 1. Configure Upstream Brokers

Edit the add-on configuration with your upstream MQTT broker details.

### 2. Start the Add-on

The unified broker will:
- Listen on `localhost:1883` (or your configured port)
- Connect to all upstream brokers
- Start forwarding messages with loop prevention

### 3. Point Home Assistant to Local Broker

In your Home Assistant `configuration.yaml`:

```yaml
mqtt:
  broker: localhost
  port: 1883
  # No username/password needed for local connection
```

Restart Home Assistant.

### 4. Verify

Check add-on logs for:
```
[INFO] === HA MQTT Unifier Ready ===
[INFO] Local MQTT broker listening on 0.0.0.0:1883
[INFO] Upstream upstream_a connected: 192.168.1.10:1883
[INFO] Upstream upstream_b connected: 192.168.1.11:1883
```

## License

MIT License - see [LICENSE](../LICENSE)

## Support

- **Issues**: [GitHub Issues](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/issues)

[releases-shield]: https://img.shields.io/github/release/ussdeveloper/home-assistant-addons-mqtt-mirror-link.svg
[releases]: https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/releases
[license-shield]: https://img.shields.io/github/license/ussdeveloper/home-assistant-addons-mqtt-mirror-link.svg
