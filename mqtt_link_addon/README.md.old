# MQTT Mirror Link Add-on

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]
![Supports armhf Architecture][armhf-shield]
![Supports armv7 Architecture][armv7-shield]
![Supports i386 Architecture][i386-shield]

Synchronizuj komunikaty MQTT między dwoma brokerami - linkuj dwie instancje Home Assistant!

## 🎯 Funkcje

- ✅ Synchronizacja dwukierunkowa (A ↔ B)
- ✅ Synchronizacja jednokierunkowa (A → B)
- ✅ Filtrowanie tematów MQTT
- ✅ Uwierzytelnianie
- ✅ Zachowanie QoS i retain

## ⚙️ Konfiguracja

### Broker A (lokalny)
- **host**: Adres brokera A (domyślnie: localhost)
- **port**: Port MQTT (domyślnie: 1883)
- **username**: Login (opcjonalnie)
- **password**: Hasło (opcjonalnie)
- **topic**: Temat do subskrypcji (domyślnie: #)

### Broker B (zdalny)
- **host**: Adres brokera B (wymagane!)
- **port**: Port MQTT (domyślnie: 1883)
- **username**: Login (opcjonalnie)
- **password**: Hasło (opcjonalnie)
- **topic**: Temat do subskrypcji (domyślnie: #)

### Opcje
- **bidirectional**: Synchronizacja dwukierunkowa (domyślnie: true)
- **log_level**: Poziom logowania (debug, info, warning, error)

## 📖 Przykład konfiguracji

```json
{
  "broker_a": {
    "host": "localhost",
    "port": 1883,
    "topic": "homeassistant/#"
  },
  "broker_b": {
    "host": "192.168.1.100",
    "port": 1883,
    "topic": "homeassistant/#"
  },
  "bidirectional": true,
  "log_level": "info"
}
```

## 🚀 Użycie

1. Zainstaluj dodatek
2. Skonfiguruj oba brokery
3. Uruchom dodatek
4. Sprawdź logi

## 📝 Dokumentacja

Pełna dokumentacja: https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg
