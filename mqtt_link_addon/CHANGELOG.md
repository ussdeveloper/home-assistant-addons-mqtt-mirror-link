## What's changed

🎉 **Pierwsza wersja MQTT Mirror Link Add-on dla Home Assistant!**

### ✨ Funkcje
- ✅ Synchronizacja dwukierunkowa komunikatów MQTT między dwoma brokerami
- ✅ Synchronizacja jednokierunkowa (opcjonalnie)
- ✅ Filtrowanie tematów MQTT (wildcard support: `#`, `+`)
- ✅ Pełne uwierzytelnianie MQTT (username/password)
- ✅ Zachowanie QoS i retain flags
- ✅ Konfiguracja przez Home Assistant UI
- ✅ Wsparcie dla wszystkich architektur (aarch64, amd64, armhf, armv7, i386)

### 📦 Instalacja

#### Jako Add-on Repository
1. W Home Assistant przejdź do **Settings** → **Add-ons**
2. Kliknij **Add-on Store** (prawy dolny róg)
3. Menu **⋮** → **Repositories**
4. Dodaj: `https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link`
5. Znajdź **MQTT Mirror Link** i zainstaluj

#### Jako Custom Integration (HACS)
1. Otwórz HACS → Integrations
2. Menu (⋮) → Custom repositories
3. URL: `https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link`
4. Kategoria: Integration

### 🔧 Konfiguracja

Po instalacji:
1. Otwórz dodatek
2. Przejdź do zakładki **Configuration**
3. Skonfiguruj oba brokery MQTT
4. Zapisz i uruchom dodatek

### 📚 Dokumentacja
- [README.md](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/blob/main/README.md)
- [Przykłady konfiguracji](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/blob/main/EXAMPLES.md)
- [Testy](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/blob/main/TESTING.md)
