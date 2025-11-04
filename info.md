# MQTT Mirror Link

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub Release](https://img.shields.io/github/release/ussdeveloper/home-assistant-addons-mqtt-mirror-link.svg)](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/releases)
[![License](https://img.shields.io/github/license/ussdeveloper/home-assistant-addons-mqtt-mirror-link.svg)](LICENSE)

Synchronizacja komunikatów MQTT między dwoma brokerami - linkuj dwie instancje Home Assistant przez MQTT!

## 🎯 Co to robi?

MQTT Mirror Link to custom integration dla Home Assistant, która działa jak most (bridge) między dwoma brokerami MQTT. Dzięki niej możesz:

- 🔄 **Synchronizować** wszystkie komunikaty MQTT między dwoma Home Assistant
- 📡 **Linkować** zdalne urządzenia IoT
- 🏠 **Replikować** stan z jednej instancji do drugiej
- ⚡ **Otrzymywać** aktualizacje w czasie rzeczywistym

## ✨ Funkcje

- ✅ Synchronizacja **dwukierunkowa** (A ↔ B)
- ✅ Synchronizacja **jednokierunkowa** (A → B)
- ✅ **Filtrowanie tematów** (wybierz co synchronizować)
- ✅ Pełne **uwierzytelnianie** MQTT
- ✅ Zachowanie **QoS i retain flags**
- ✅ Konfiguracja przez **UI** (bez YAML!)
- ✅ Automatyczne **reconnect** po utracie połączenia

## 📦 Instalacja

### HACS (zalecana)

1. Otwórz **HACS** w Home Assistant
2. Przejdź do **Integrations**
3. Kliknij menu **⋮** (prawym górnym rogu)
4. Wybierz **Custom repositories**
5. Wklej URL: `https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link`
6. Kategoria: **Integration**
7. Kliknij **Add**
8. Znajdź **MQTT Mirror Link** i kliknij **Download**
9. **Zrestartuj** Home Assistant

### Instalacja manualna

1. Skopiuj folder `custom_components/mqtt_link` do swojego Home Assistant:
   ```
   <config_dir>/custom_components/mqtt_link/
   ```
2. Zrestartuj Home Assistant

## ⚙️ Konfiguracja

### Szybki start

1. Przejdź do **Ustawienia** → **Urządzenia i usługi**
2. Kliknij **+ DODAJ INTEGRACJĘ**
3. Wyszukaj **MQTT Mirror Link**
4. Podaj dane dla **Brokera A** (lokalny HA):
   - Host: `localhost`
   - Port: `1883`
   - Temat: `#` (wszystkie)
5. Podaj dane dla **Brokera B** (zdalny HA):
   - Host: `192.168.1.100` (IP drugiego HA)
   - Port: `1883`
   - Temat: `#` (wszystkie)
   - ✓ Synchronizacja dwukierunkowa

Gotowe! 🎉

## 💡 Przykłady użycia

### Przykład 1: Pełna synchronizacja dwóch Home Assistant

```
HA-A (192.168.1.10) ←→ HA-B (192.168.1.20)
Wszystkie komunikaty MQTT są zsynchronizowane
```

**Broker A:**
- Host: `localhost`
- Temat: `#`

**Broker B:**
- Host: `192.168.1.20`
- Temat: `#`
- Dwukierunkowa: ✓

### Przykład 2: Synchronizacja tylko urządzeń Home Assistant

```
Tylko discovery i state urządzeń HA
```

**Oba brokery:**
- Temat: `homeassistant/#`

### Przykład 3: Backup jednokierunkowy

```
HA-Primary → HA-Backup (tylko odczyt)
```

**Broker B:**
- Dwukierunkowa: ✗

## 🔧 Opcje konfiguracji

| Parametr | Opis | Domyślnie |
|----------|------|-----------|
| `broker_a_host` | Adres IP/hostname brokera A | `localhost` |
| `broker_a_port` | Port MQTT brokera A | `1883` |
| `broker_a_username` | Login do brokera A | - |
| `broker_a_password` | Hasło do brokera A | - |
| `broker_a_topic` | Temat MQTT do subskrypcji | `#` |
| `broker_b_host` | Adres IP/hostname brokera B | **wymagane** |
| `broker_b_port` | Port MQTT brokera B | `1883` |
| `broker_b_username` | Login do brokera B | - |
| `broker_b_password` | Hasło do brokera B | - |
| `broker_b_topic` | Temat MQTT do subskrypcji | `#` |
| `bidirectional` | Synchronizacja w obie strony | `true` |

## 🐛 Rozwiązywanie problemów

### Debug logging

Włącz szczegółowe logi w `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.mqtt_link: debug
```

### FAQ

**Q: Komunikaty się duplikują!**  
A: Użyj różnych tematów lub wyłącz synchronizację dwukierunkową.

**Q: Nie łączy się z brokerem**  
A: Sprawdź firewall, uprawnienia i dane logowania.

**Q: Jak synchronizować tylko wybrane urządzenia?**  
A: Użyj konkretnych tematów, np. `homeassistant/sensor/#`

## 📝 Changelog

### v1.0.0 (2025-11-04)
- 🎉 Pierwsza wersja publiczna
- ✅ Synchronizacja dwukierunkowa
- ✅ Konfiguracja przez UI
- ✅ Filtrowanie tematów
- ✅ Uwierzytelnianie MQTT

## 📄 Licencja

MIT License - zobacz [LICENSE](LICENSE)

## 🤝 Wsparcie

- 🐛 **Issues**: [GitHub Issues](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/issues)
- 💬 **Dyskusje**: [GitHub Discussions](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/discussions)

## ⭐ Podoba Ci się?

Zostaw ⭐ na [GitHub](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link)!
