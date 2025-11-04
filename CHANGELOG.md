# Changelog

Wszystkie znaczące zmiany w tym projekcie będą dokumentowane w tym pliku.

Format oparty na [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
projekt przestrzega [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Brak zaplanowanych zmian.

## [1.0.0] - 2025-11-04

### 🎉 Pierwsza wersja publiczna

#### Added
- ✅ Synchronizacja dwukierunkowa komunikatów MQTT między dwoma brokerami
- ✅ Opcja synchronizacji jednokierunkowej (A→B tylko)
- ✅ Konfiguracja przez UI Home Assistant (config flow)
- ✅ Filtrowanie tematów MQTT (wildcard support: `#`, `+`)
- ✅ Pełne uwierzytelnianie MQTT (username/password)
- ✅ Zachowanie QoS flags (0, 1, 2)
- ✅ Zachowanie retain flags
- ✅ Automatyczne reconnect po utracie połączenia
- ✅ Wsparcie dla HACS (Home Assistant Community Store)
- ✅ Dokumentacja PL/EN
- ✅ Przykłady konfiguracji
- ✅ CI/CD pipeline (GitHub Actions)

#### Documentation
- 📖 README.md z pełną dokumentacją
- 📖 QUICKSTART.md - szybki start
- 📖 EXAMPLES.md - przykłady użycia
- 📖 PUBLICATION_GUIDE.md - przewodnik publikacji
- 📖 CONTRIBUTING.md - przewodnik dla developerów
- 📖 info.md - opis dla HACS

#### Infrastructure
- 🔧 GitHub Actions workflows (validate, release)
- 🔧 HACS integration (hacs.json)
- 🔧 License (MIT)
- 🔧 .gitignore

---

## Planowane funkcje (roadmap)

### [1.1.0] - TBD
- [ ] Wsparcie dla MQTT 5
- [ ] QoS filtering
- [ ] Statistics i monitoring
- [ ] UI diagnostyki

### [1.2.0] - TBD
- [ ] Topic transformations
- [ ] Payload filtering/modification
- [ ] Multiple brokers (więcej niż 2)

### [2.0.0] - TBD
- [ ] Docker standalone version
- [ ] Web UI
- [ ] REST API

---

## Format zmian

### Categories
- **Added**: Nowe funkcje
- **Changed**: Zmiany w istniejącej funkcjonalności
- **Deprecated**: Funkcje do usunięcia w przyszłości
- **Removed**: Usunięte funkcje
- **Fixed**: Naprawione błędy
- **Security**: Łatki bezpieczeństwa

### Przykład wpisu
```markdown
## [1.1.0] - 2025-12-01

### Added
- Wsparcie dla MQTT 5 protocol
- QoS filtering w konfiguracji

### Fixed
- Naprawiono pętlę komunikatów przy bidirectional sync
- Poprawiono memory leak przy długim działaniu

### Changed
- Zaktualizowano paho-mqtt do 2.0.0
```

---

## Historia rozwoju

- **2025-11-04**: Pierwsza wersja publiczna (v1.0.0)
- **2025-11-03**: Rozpoczęcie projektu

---

## Linki

- [Releases](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/releases)
- [Issues](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/issues)
- [Pull Requests](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/pulls)

---

**[Unreleased]**: https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/compare/v1.0.0...HEAD
**[1.0.0]**: https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/releases/tag/v1.0.0
