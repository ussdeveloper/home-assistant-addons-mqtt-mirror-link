# MQTT Mirror Link

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub Release](https://img.shields.io/github/release/ussdeveloper/home-assistant-addons-mqtt-mirror-link.svg)](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/releases)
[![License](https://img.shields.io/github/license/ussdeveloper/home-assistant-addons-mqtt-mirror-link.svg)](LICENSE)

**Synchronizacja komunikatów MQTT między dwoma brokerami - linkuj dwie instancje Home Assistant przez MQTT!**

## 📚 Dokumentacja

- 🚀 [QUICKSTART.md](QUICKSTART.md) - Szybki start (3 kroki do działania!)
- 📖 [EXAMPLES.md](EXAMPLES.md) - 10+ przykładów konfiguracji
- 📝 [PUBLICATION_GUIDE.md](PUBLICATION_GUIDE.md) - Jak opublikować na GitHub
- ✅ [CHECKLIST.md](CHECKLIST.md) - Lista kontrolna przed publikacją
- 🤝 [CONTRIBUTING.md](CONTRIBUTING.md) - Jak pomóc w rozwoju
- 📋 [CHANGELOG.md](CHANGELOG.md) - Historia zmian

## 🎯 Co to robi?

MQTT Mirror Link to custom integration dla Home Assistant, która działa jak most (bridge) między dwoma brokerami MQTT. Dzięki niej możesz linkować dwie instancje Home Assistant przez MQTT, tak aby wszystkie komunikaty z jednej instancji były automatycznie przekazywane do drugiej.

## ✨ Funkcje

- ✅ **Synchronizacja dwukierunkowa** - komunikaty mogą przepływać w obie strony (A→B i B→A)
- ✅ **Synchronizacja jednokierunkowa** - możliwość ustawienia przepływu tylko w jednym kierunku
- ✅ **Filtrowanie tematów** - subskrybuj tylko wybrane tematy MQTT (np. `homeassistant/#`)
- ✅ **Uwierzytelnianie** - pełne wsparcie dla loginu i hasła MQTT
- ✅ **Konfiguracja przez UI** - łatwa konfiguracja przez interfejs Home Assistant
- ✅ **Zachowanie QoS i retain** - wszystkie atrybuty wiadomości są zachowywane
- ✅ **Automatyczne reconnect** - po utracie połączenia

## 📦 Instalacja

### Metoda 1: Home Assistant Add-on (zalecana) ⭐

1. W Home Assistant przejdź do **Settings** → **Add-ons**
2. Kliknij **Add-on Store** (prawy dolny róg)
3. Menu **⋮** (prawy górny róg) → **Repositories**
4. Dodaj URL: `https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link`
5. Znajdź **MQTT Mirror Link** i kliknij
6. Kliknij **INSTALL**
7. Skonfiguruj i uruchom

### Metoda 2: HACS Custom Integration

1. Otwórz **HACS** w Home Assistant
2. Przejdź do **Integrations**
3. Kliknij menu **⋮** (prawym górnym rogu)
4. Wybierz **Custom repositories**
5. Wklej URL: `https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link`
6. Kategoria: **Integration**
7. Kliknij **Add**
8. Znajdź **MQTT Mirror Link** i kliknij **Download**
9. **Zrestartuj** Home Assistant

### Metoda 3: Instalacja manualna

1. Pobierz najnowszą wersję z [Releases](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/releases)
2. Rozpakuj i skopiuj folder `custom_components/mqtt_link` do katalogu `custom_components` w Home Assistant:
   ```
   <config_dir>/custom_components/mqtt_link/
   ```
3. Zrestartuj Home Assistant

## Konfiguracja

### Krok 1: Dodaj integrację

1. W Home Assistant przejdź do **Ustawienia** → **Urządzenia i usługi**
2. Kliknij **+ DODAJ INTEGRACJĘ**
3. Wyszukaj **MQTT Link**

### Krok 2: Skonfiguruj Broker A (lokalny)

Podaj dane połączenia do pierwszego brokera MQTT (zazwyczaj lokalny Home Assistant):

- **Host**: adres IP lub hostname (domyślnie: `localhost`)
- **Port**: port MQTT (domyślnie: `1883`)
- **Użytkownik**: nazwa użytkownika (opcjonalnie)
- **Hasło**: hasło (opcjonalnie)
- **Temat**: temat MQTT do subskrypcji (domyślnie: `#` - wszystkie tematy)

### Krok 3: Skonfiguruj Broker B (zdalny)

Podaj dane połączenia do drugiego brokera MQTT (zdalny Home Assistant):

- **Host**: adres IP lub hostname zdalnego Home Assistant
- **Port**: port MQTT (domyślnie: `1883`)
- **Użytkownik**: nazwa użytkownika (opcjonalnie)
- **Hasło**: hasło (opcjonalnie)
- **Temat**: temat MQTT do subskrypcji (domyślnie: `#` - wszystkie tematy)
- **Synchronizacja dwukierunkowa**: czy komunikaty mają płynąć w obie strony (domyślnie: TAK)

## Przykłady użycia

### Przykład 1: Pełna synchronizacja dwóch Home Assistant

**Home Assistant A** (lokalny):
- Host: `localhost`
- Port: `1883`
- Temat: `#`

**Home Assistant B** (zdalny):
- Host: `192.168.1.100`
- Port: `1883`
- Temat: `#`
- Synchronizacja dwukierunkowa: ✓

Rezultat: Wszystkie komunikaty MQTT z obu instancji będą zsynchronizowane.

### Przykład 2: Synchronizacja tylko urządzeń Home Assistant

**Home Assistant A**:
- Temat: `homeassistant/#`

**Home Assistant B**:
- Temat: `homeassistant/#`

Rezultat: Tylko komunikaty związane z urządzeniami Home Assistant będą synchronizowane.

### Przykład 3: Jednokierunkowa synchronizacja

**Home Assistant A** → **Home Assistant B**:
- Synchronizacja dwukierunkowa: ✗

Rezultat: Komunikaty płyną tylko z A do B, ale nie odwrotnie.

## Rozwiązywanie problemów

### Sprawdź logi

Włącz szczegółowe logowanie w `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.mqtt_link: debug
```

### Typowe problemy

**Problem**: Integracja nie łączy się z brokerem
- Sprawdź, czy broker MQTT jest uruchomiony
- Sprawdź dane logowania (użytkownik/hasło)
- Sprawdź firewall i porty

**Problem**: Komunikaty się nie synchronizują
- Sprawdź, czy tematy są poprawnie skonfigurowane
- Upewnij się, że broker ma uprawnienia do publikacji/subskrypcji
- Sprawdź logi pod kątem błędów

**Problem**: Pętla komunikatów (duplikaty)
- Użyj różnych tematów dla każdego brokera
- Lub wyłącz synchronizację dwukierunkową

## 📝 Changelog

### v1.0.0 (2025-11-04)
- 🎉 Pierwsza wersja publiczna
- ✅ Synchronizacja dwukierunkowa MQTT
- ✅ Konfiguracja przez UI
- ✅ Wsparcie dla uwierzytelniania
- ✅ Filtrowanie tematów

## 📄 Licencja

MIT License - zobacz [LICENSE](LICENSE)

## 🤝 Wsparcie

- 🐛 **Issues**: [GitHub Issues](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/issues)
- 💬 **Dyskusje**: [GitHub Discussions](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/discussions)

## 🚀 Jak opublikować na GitHub

1. **Utwórz nowe repozytorium** na GitHub o nazwie `home-assistant-addons-mqtt-mirror-link`

2. **Wypchnij pliki** do repozytorium:

```bash
cd "c:\Users\sulaco\Desktop\HomeAssistant MQTT LINK"
git init
git add .
git commit -m "Initial commit: MQTT Mirror Link v1.0.0"
git branch -M main
git remote add origin https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link.git
git push -u origin main
```

3. **Utwórz release**:
   - Przejdź do **Releases** → **Create a new release**
   - Tag: `v1.0.0`
   - Title: `v1.0.0 - Initial Release`
   - Description: Skopiuj opis z README
   - Opublikuj!

4. **Dodaj do HACS** w Home Assistant:
   - Otwórz HACS → Integrations
   - Menu (⋮) → Custom repositories
   - URL: `https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link`
   - Kategoria: Integration
   - Teraz możesz zainstalować dodatek!

## ⭐ Podoba Ci się?

Zostaw ⭐ na [GitHub](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link)!
