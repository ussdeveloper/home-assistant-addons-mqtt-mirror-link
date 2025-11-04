# MQTT Mirror Link - Home Assistant Add-on

[![GitHub Release](https://img.shields.io/github/release/ussdeveloper/home-assistant-addons-mqtt-mirror-link.svg)](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/releases)
[![License](https://img.shields.io/github/license/ussdeveloper/home-assistant-addons-mqtt-mirror-link.svg)](LICENSE)

**Virtual unified MQTT broker for Home Assistant - connect multiple upstream brokers into one!**

## 🎯 What does it do?

MQTT Mirror Link is a Home Assistant Add-on that creates a **virtual unified MQTT broker** (local endpoint for Home Assistant). The addon internally connects to multiple upstream MQTT brokers, creating a unified message space.

### Architektura v2.0

```
Home Assistant
      ↕
Local Broker (localhost:1883)  ← This addon
      ↕              ↕
Upstream A     Upstream B
(broker 1)     (broker 2)
```

**How it works:**
- Home Assistant connects only to the local broker (this addon)
- Addon connects to multiple upstream brokers (unlimited number)
- All messages are automatically synchronized
- Built-in loop detection (LRU cache + MQTT v5 origin tagging)

## ✨ Features

- ✅ **Virtual unified broker** - single endpoint for Home Assistant
- ✅ **Multiple upstream brokers** - unlimited number of connections
- ✅ **Automatic loop detection** - sha1 hashing + LRU cache (50k messages, 30s TTL)
- ✅ **MQTT v5 origin tagging** - user properties for source tracking
- ✅ **Fan-in/fan-out routing** - local→all upstreams, upstream A→local+upstream B
- ✅ **$SYS/# filtering** - excludes broker system topics
- ✅ **Authentication** - full username/password support
- ✅ **Automatic reconnect** - after connection loss
- ✅ **Node.js 20 + TypeScript** - modern technology stack

## 📦 Installation

1. In Home Assistant go to **Settings** → **Add-ons**
2. Click **Add-on Store** (bottom right corner)
3. Menu **⋮** (top right corner) → **Repositories**
4. Add URL: `https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link`
5. Find **MQTT Mirror Link** and click **INSTALL**
6. Go to **Configuration** tab
7. Configure (see examples below)
8. Start the addon (**Info** tab → **START**)

## ⚙️ Configuration

### Local Broker Parameters

- **listen.host** - IP address for local broker to listen on (default: `0.0.0.0`)
- **listen.port** - Local broker port (default: `1883`)

### Upstream Broker Parameters

The `upstreams` array contains a list of brokers to connect to:

```yaml
upstreams:
  - host: "192.168.1.100"
    port: 1883
    username: "mqtt_user"
    password: "mqtt_pass"
    topics: ["#"]
    client_id: "ha-mqtt-unifier-upstream-1"
    
  - host: "192.168.1.200"
    port: 1883
    username: "mqtt_user2"
    password: "mqtt_pass2"
    topics: ["homeassistant/#", "zigbee2mqtt/#"]
    client_id: "ha-mqtt-unifier-upstream-2"
```

**Each upstream broker:**
- `host` - IP address or hostname
- `port` - MQTT port (default: 1883)
- `username` - username (optional)
- `password` - password (optional)
- `topics` - list of topics to subscribe to (default: ["#"])
- `client_id` - unique MQTT client ID

### Additional Parameters

- **discovery_prefix** - Home Assistant discovery prefix (default: `homeassistant`)
- **retain_cache_ttl_sec** - Cache TTL for retained messages (default: 30)
- **max_lru** - Maximum LRU cache size (default: 50000)

## 📋 Configuration Examples

### Example 1: Two MQTT Brokers - Full Synchronization

```yaml
upstreams:
  - host: "192.168.1.100"
    port: 1883
    username: "mqtt"
    password: "secret1"
    topics: ["#"]
    client_id: "ha-unifier-broker1"
    
  - host: "192.168.1.200"
    port: 1883
    username: "mqtt"
    password: "secret2"
    topics: ["#"]
    client_id: "ha-unifier-broker2"
```

### Example 2: Home Assistant and Zigbee2MQTT Topics Only

```yaml
upstreams:
  - host: "192.168.1.100"
    port: 1883
    topics: 
      - "homeassistant/#"
      - "zigbee2mqtt/#"
    client_id: "ha-unifier-filtered"
```

### Example 3: Three Brokers - Different Ports

```yaml
upstreams:
  - host: "mqtt.home.local"
    port: 1883
    topics: ["#"]
    
  - host: "mqtt.cloud.com"
    port: 8883
    username: "cloud_user"
    password: "cloud_pass"
    topics: ["cloud/#"]
    
  - host: "192.168.1.150"
    port: 1884
    topics: ["sensors/#"]
```

### Home Assistant Configuration

After starting the addon, configure Home Assistant to connect to the local broker:

**configuration.yaml:**
```yaml
mqtt:
  broker: localhost
  port: 1883
  # username/password if required by upstream brokers
```

## 🔧 Troubleshooting

### Check Addon Logs

In Home Assistant:
1. Go to **Settings** → **Add-ons** → **MQTT Mirror Link**
2. **Log** tab - check for connection errors with upstream brokers

### Common Issues

**Issue**: Addon won't start
- Check addon logs
- Ensure YAML configuration format is correct
- Check if port 1883 is already in use

**Issue**: Home Assistant won't connect to local broker
- Ensure addon is running (status: **Running**)
- Check `configuration.yaml` - broker should be `localhost:1883`
- Restart Home Assistant after changing MQTT configuration

**Issue**: No synchronization with upstream brokers
- Check login credentials (username/password)
- Check network availability (ping upstream brokers)
- Check firewall and MQTT user permissions
- Check addon logs - you'll see connection errors

**Issue**: Duplicate messages
- Shouldn't happen - addon has built-in loop detection
- If it occurs, increase `retain_cache_ttl_sec`
- Check logs - you'll see "Ignoring duplicate message" when detection works

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for full change history.

**Latest version: v2.0.2**
- Complete architecture redesign (virtual unified broker)
- Node.js 20 + TypeScript + Aedes + mqtt.js
- LRU cache deduplication + MQTT v5 origin tagging
- Unlimited number of upstream brokers

## 🛠️ Stack Technologiczny

- **Node.js 20** - runtime environment
- **TypeScript 5.6** - type-safe development
- **Aedes 0.51.3** - lightweight MQTT broker library
- **mqtt.js 5.10.1** - MQTT v5 client library
- **lru-cache 10.4.3** - message deduplication
- **Alpine Linux 3.20** - Docker base image

## 📄 License

MIT License - see [LICENSE](LICENSE)

## 🤝 Support

- 🐛 **Report Issue**: [GitHub Issues](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/issues)
- 💬 **Discussion**: [GitHub Discussions](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/discussions)

## ⭐ Like it?

Leave a ⭐ on [GitHub](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link)!
