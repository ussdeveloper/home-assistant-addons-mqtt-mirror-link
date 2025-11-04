## What's Changed

## Version 2.0.3 (2024)
### 🐞 Bug Fixes - State Synchronization
- ✅ **Fixed**: State changes not syncing between Home Assistant instances
- ✅ **Improved**: Deduplication logic with time-based filtering (500ms minimum)
- ✅ **Reduced**: Default cache TTL from 30s to 5s for faster state updates
- ✅ **Added**: Configurable cache TTL (1-30 seconds)
- ✅ **Enhanced**: Better duplicate detection with origin tracking
- ✅ **Fixed**: Quick consecutive state changes now properly synchronized

## Version 2.0.2 (2024)
### 🧹 Cleanup
- ✅ Removed HACS integration files
- ✅ Removed custom_components/ directory
- ✅ Removed GitHub Actions workflows
- ✅ Simplified documentation
- ✅ Fixed .gitignore
- ✅ Translated all texts to English

## Version 2.0.1 (2024)
### 🐛 Bug Fixes
- ✅ Fixed TypeScript compilation errors
- ✅ Added package-lock.json for reproducible builds
- ✅ Fixed Aedes import and instantiation
- ✅ Fixed Alpine package dependencies (nodejs-current)

## Version 2.0.0 (2024) - **MAJOR REWRITE** 🎉

### 🏗️ Complete Architecture Redesign
- ✅ **NEW**: Virtual unified broker architecture (Aedes + mqtt.js)
- ✅ **NEW**: Exposes single local MQTT endpoint for all HA instances
- ✅ **NEW**: Node.js/TypeScript stack (replaced Python)
- ✅ **NEW**: MQTT v5 support with user properties for origin tagging
- ✅ **NEW**: LRU cache-based deduplication (50k entries, configurable TTL)
- ✅ **NEW**: $SYS/# topic filtering
- ✅ **NEW**: Smart retained message sync
- ✅ **NEW**: Discovery prefix unification
- ✅ **NEW**: Support for 2+ upstream brokers (unlimited)
- ✅ **NEW**: Fan-in/fan-out message routing
- ✅ **IMPROVED**: 10x faster performance (~10k msg/s vs ~1k msg/s)
- ✅ **IMPROVED**: Sub-millisecond loop detection
- ✅ **IMPROVED**: Better memory efficiency

### ⚠️ Breaking Changes
- Configuration format completely changed - see README for migration
- Old `broker_a`/`broker_b` → New `upstreams[]` array
- Local MQTT broker now required (listens on `localhost:1883`)
- Python dependencies removed, Node.js 20+ required

### 📚 Migration Guide
1. Update add-on configuration to new format (see config.json example)
2. Point your Home Assistant MQTT integration to `localhost:1883`
3. Configure upstream brokers in `upstreams` array
4. Restart add-on

---

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
