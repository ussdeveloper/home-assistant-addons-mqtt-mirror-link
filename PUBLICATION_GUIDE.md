# Instrukcje publikacji repozytorium na GitHub

## Krok 1: Utwórz repozytorium na GitHub

1. Przejdź na https://github.com/new
2. Repository name: `home-assistant-addons-mqtt-mirror-link`
3. Description: `🔄 MQTT Mirror Link - Synchronizuj komunikaty MQTT między dwoma Home Assistant`
4. Public
5. **NIE** dodawaj README, .gitignore ani LICENSE (już są w projekcie)
6. Kliknij **Create repository**

## Krok 2: Wypchnij kod do GitHub

Otwórz PowerShell w folderze projektu i wykonaj:

```powershell
# Przejdź do katalogu projektu
cd "c:\Users\sulaco\Desktop\HomeAssistant MQTT LINK"

# Zainicjuj Git
git init

# Dodaj wszystkie pliki
git add .

# Pierwszy commit
git commit -m "Initial commit: MQTT Mirror Link v1.0.0

- Synchronizacja dwukierunkowa MQTT
- Konfiguracja przez UI Home Assistant
- Filtrowanie tematów
- Uwierzytelnianie MQTT
- Dokumentacja PL/EN"

# Ustaw główną gałąź
git branch -M main

# Dodaj zdalne repozytorium (zmień 'ussdeveloper' na swoją nazwę użytkownika!)
git remote add origin https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link.git

# Wypchnij kod
git push -u origin main
```

## Krok 3: Utwórz pierwszy Release

1. Przejdź do repozytorium na GitHub
2. Kliknij **Releases** (prawa strona)
3. Kliknij **Create a new release**
4. Wypełnij formularz:
   - **Tag**: `v1.0.0`
   - **Release title**: `v1.0.0 - Initial Release 🎉`
   - **Description**:
   ```markdown
   ## 🎉 Pierwsza wersja MQTT Mirror Link!
   
   ### ✨ Funkcje
   - ✅ Synchronizacja dwukierunkowa komunikatów MQTT
   - ✅ Synchronizacja jednokierunkowa (opcjonalnie)
   - ✅ Konfiguracja przez interfejs Home Assistant UI
   - ✅ Filtrowanie tematów MQTT
   - ✅ Pełne uwierzytelnianie (username/password)
   - ✅ Zachowanie QoS i retain flags
   - ✅ Automatyczne reconnect
   
   ### 📦 Instalacja
   
   #### HACS (zalecana)
   1. Otwórz HACS → Integrations
   2. Menu (⋮) → Custom repositories
   3. URL: `https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link`
   4. Kategoria: Integration
   5. Pobierz i zrestartuj HA
   
   #### Manualna
   1. Pobierz `mqtt_link.zip` poniżej
   2. Rozpakuj do `<config>/custom_components/`
   3. Zrestartuj Home Assistant
   
   ### 📚 Dokumentacja
   Zobacz [README.md](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link#readme)
   ```
5. Kliknij **Publish release**

## Krok 4: Dodaj do HACS w Home Assistant

Teraz możesz dodać repozytorium do HACS:

1. Otwórz Home Assistant
2. Przejdź do **HACS** → **Integrations**
3. Kliknij menu **⋮** (prawy górny róg)
4. Wybierz **Custom repositories**
5. Wklej: `https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link`
6. Kategoria: **Integration**
7. Kliknij **Add**
8. Znajdź **MQTT Mirror Link** na liście
9. Kliknij **Download**
10. Zrestartuj Home Assistant

## Krok 5: Skonfiguruj integrację

1. Przejdź do **Ustawienia** → **Urządzenia i usługi**
2. Kliknij **+ DODAJ INTEGRACJĘ**
3. Wyszukaj **MQTT Mirror Link**
4. Postępuj zgodnie z instrukcjami w README.md

## 🎉 Gotowe!

Twoje repozytorium jest teraz publiczne i gotowe do instalacji przez HACS!

## Przydatne komendy Git

### Aktualizacja kodu
```powershell
git add .
git commit -m "Opis zmian"
git push
```

### Nowy release
```powershell
# Utwórz tag
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin v1.1.0

# Potem utwórz Release na GitHub z tego tagu
```

### Sprawdzenie statusu
```powershell
git status
git log --oneline -5
```
