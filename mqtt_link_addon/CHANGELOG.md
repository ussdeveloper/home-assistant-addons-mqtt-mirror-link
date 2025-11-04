## What's changed

## Version 1.0.4 (2024)
### 🔧 Loop Prevention Fix
- ✅ Fixed loop detection algorithm to work correctly with mirror link
- ✅ Changed from direction-based to broker-based loop detection
- ✅ Now allows legitimate duplicate messages while preventing infinite loops
- ✅ Improved: A→B→A loop prevention without blocking A→B, A→B sequences

## Version 1.0.3 (2024)
### 🛡️ Loop Prevention
- ✅ Added message loop prevention mechanism
- ✅ Message deduplication using MD5 hashing
- ✅ Configurable message TTL (Time-To-Live) for duplicate detection
- ✅ New configuration options:
  - `loop_prevention`: Enable/disable loop detection (default: true)
  - `message_ttl`: Time window for duplicate detection in seconds (1-10, default: 2)

## Version 1.0.2 (2024)
### 🐛 Bug Fixes
- ✅ Fixed Docker base image references
- ✅ Corrected Python3 installation in Dockerfile

## Version 1.0.1 (2024)
### 🌍 Localization
- ✅ Translated all Polish comments and documentation to English
- ✅ Updated UI strings to English

## Version 1.0.0 (2024)
🎉 **First release of MQTT Mirror Link Add-on for Home Assistant!**

### ✨ Features
- ✅ Bidirectional MQTT message synchronization between two brokers
- ✅ Unidirectional synchronization (optional)
- ✅ MQTT topic filtering (wildcard support: `#`, `+`)
- ✅ Full MQTT authentication (username/password)
- ✅ Preserve QoS and retain flags
- ✅ Configuration through Home Assistant UI
- ✅ Support for all architectures (aarch64, amd64, armhf, armv7, i386)

### 📦 Installation

#### As Add-on Repository
1. In Home Assistant go to **Settings** → **Add-ons**
2. Click **Add-on Store** (bottom right)
3. Menu **⋮** → **Repositories**
4. Add: `https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link`
5. Find **MQTT Mirror Link** and install

#### As Custom Integration (HACS)
1. Open HACS → Integrations
2. Menu (⋮) → Custom repositories
3. URL: `https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link`
4. Category: Integration

### 🔧 Configuration

After installation:
1. Open the add-on
2. Go to **Configuration** tab
3. Configure both MQTT brokers
4. Save and start the add-on

### 📚 Documentation
- [README.md](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/blob/main/README.md)
- [Configuration Examples](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/blob/main/EXAMPLES.md)
- [Testing](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/blob/main/TESTING.md)
