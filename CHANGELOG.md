# Changelog

Wszystkie znaczące zmiany w tym projekcie będą dokumentowane w tym pliku.

Format oparty na [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
projekt przestrzega [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Brak zaplanowanych zmian.

## [1.0.0] - 2025-11-04

### 🎉 First Public Release

#### Added
- ✅ Bidirectional MQTT message synchronization between two brokers
- ✅ Unidirectional synchronization option (A→B only)
- ✅ Configuration via Home Assistant UI (config flow)
- ✅ MQTT topic filtering (wildcard support: `#`, `+`)
- ✅ Full MQTT authentication (username/password)
- ✅ QoS flags preservation (0, 1, 2)
- ✅ Retain flags preservation
- ✅ Automatic reconnect after connection loss
- ✅ HACS support (Home Assistant Community Store)
- ✅ Documentation in PL/EN
- ✅ Configuration examples
- ✅ CI/CD pipeline (GitHub Actions)

#### Documentation
- 📖 README.md with full documentation
- 📖 QUICKSTART.md - quick start guide
- 📖 EXAMPLES.md - usage examples
- 📖 PUBLICATION_GUIDE.md - publication guide
- 📖 CONTRIBUTING.md - developer guide
- 📖 info.md - HACS description

#### Infrastructure
- 🔧 GitHub Actions workflows (validate, release)
- 🔧 HACS integration (hacs.json)
- 🔧 License (MIT)
- 🔧 .gitignore

---

## Planned Features (Roadmap)

### [3.0.0] - TBD
- [ ] Enhanced statistics and monitoring
- [ ] Web UI for configuration
- [ ] Topic transformations
- [ ] Payload filtering/modification

---

## Change Format

### Categories
- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Features to be removed in the future
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security patches

### Example Entry
```markdown
## [3.0.0] - 2026-01-01

### Added
- MQTT 5 enhanced features
- QoS filtering in configuration

### Fixed
- Fixed message loop in bidirectional sync
- Fixed memory leak during long operation

### Changed
- Updated mqtt.js to 6.0.0
```

---

## Development History

- **2025-11-04**: v2.0.2 - Repository cleanup
- **2025-11-04**: v2.0.1 - Bug fixes
- **2025-11-04**: v2.0.0 - Complete rewrite (Node.js/TypeScript)
- **2025-11-04**: v1.0.0 - First public release (Python)
- **2025-11-03**: Project started

---

## Links

- [Releases](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/releases)
- [Issues](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/issues)
- [Pull Requests](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/pulls)

---

**[Unreleased]**: https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/compare/v1.0.0...HEAD
**[1.0.0]**: https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/releases/tag/v1.0.0
