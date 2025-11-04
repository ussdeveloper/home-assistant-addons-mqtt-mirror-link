# ✅ Checklist przed publikacją

## 📋 Przed wysłaniem na GitHub

### Konfiguracja osobista
- [ ] Zmień `ussdeveloper` na swoją nazwę użytkownika w:
  - [ ] `README.md`
  - [ ] `info.md`
  - [ ] `CONTRIBUTING.md`
  - [ ] `CHANGELOG.md`
  - [ ] `BADGES.md`
  - [ ] `PUBLICATION_GUIDE.md`
  - [ ] `QUICKSTART.md`
  - [ ] `custom_components/mqtt_link/manifest.json`
- [ ] Zmień `@sulaco` na `@TWOJA_NAZWA` w:
  - [ ] `custom_components/mqtt_link/manifest.json` (codeowners)

### Weryfikacja plików
- [ ] Wszystkie pliki są na miejscu (19 plików)
- [ ] `manifest.json` jest poprawny (valid JSON)
- [ ] `hacs.json` jest poprawny (valid JSON)
- [ ] LICENSE zawiera właściwe informacje
- [ ] README.md ma poprawne linki

### Przygotowanie Git
- [ ] Git jest zainstalowany (`git --version`)
- [ ] Masz konto na GitHub
- [ ] Masz utworzone repozytorium `home-assistant-addons-mqtt-mirror-link`

---

## 🚀 Publikacja

### Krok 1: Inicjalizacja
```powershell
cd "c:\Users\sulaco\Desktop\HomeAssistant MQTT LINK"
git init
git add .
git status  # Sprawdź czy wszystko jest dodane
```

### Krok 2: Commit
```powershell
git commit -m "Initial commit: MQTT Mirror Link v1.0.0"
```

### Krok 3: Remote
```powershell
git branch -M main
git remote add origin https://github.com/TWOJA_NAZWA/home-assistant-addons-mqtt-mirror-link.git
```

### Krok 4: Push
```powershell
git push -u origin main
```

**LUB użyj skryptu:**
```powershell
.\publish.ps1
```

---

## 📦 Release na GitHub

- [ ] Przejdź na https://github.com/TWOJA_NAZWA/home-assistant-addons-mqtt-mirror-link
- [ ] Kliknij **Releases** → **Create a new release**
- [ ] Tag: `v1.0.0`
- [ ] Title: `v1.0.0 - Initial Release 🎉`
- [ ] Description: Skopiuj z `CHANGELOG.md`
- [ ] Kliknij **Publish release**

---

## 🏠 Dodanie do Home Assistant

### Przez HACS
- [ ] Otwórz HACS w Home Assistant
- [ ] Integrations → Menu (⋮) → Custom repositories
- [ ] URL: `https://github.com/TWOJA_NAZWA/home-assistant-addons-mqtt-mirror-link`
- [ ] Kategoria: Integration
- [ ] Kliknij Add
- [ ] Znajdź "MQTT Mirror Link"
- [ ] Kliknij Download
- [ ] Zrestartuj Home Assistant

### Konfiguracja
- [ ] Ustawienia → Urządzenia i usługi
- [ ] + DODAJ INTEGRACJĘ
- [ ] Wyszukaj "MQTT Mirror Link"
- [ ] Skonfiguruj Broker A
- [ ] Skonfiguruj Broker B
- [ ] Kliknij Submit

---

## 🧪 Testowanie

### Po instalacji
- [ ] Integracja pojawia się w "Urządzenia i usługi"
- [ ] Brak błędów w logach
- [ ] Połączenie z brokerem A działa
- [ ] Połączenie z brokerem B działa

### Test komunikacji
- [ ] Wyślij testową wiadomość na broker A
  ```bash
  mosquitto_pub -h localhost -t test/topic -m "Hello from A"
  ```
- [ ] Sprawdź czy dotarła do brokera B
  ```bash
  mosquitto_sub -h 192.168.1.100 -t test/topic
  ```
- [ ] Jeśli bidirectional: Test w drugą stronę

### Logi debug
```yaml
# configuration.yaml
logger:
  logs:
    custom_components.mqtt_link: debug
```

- [ ] Sprawdź logi: Ustawienia → System → Logi
- [ ] Szukaj "mqtt_link"
- [ ] Sprawdź czy są komunikaty "A->B" lub "B->A"

---

## 📣 Promocja (opcjonalnie)

- [ ] Tweet/post o projekcie
- [ ] Dodaj do listy HACS
- [ ] Post na forum Home Assistant
- [ ] Reddit r/homeassistant
- [ ] YouTube demo (opcjonalnie)

---

## 🔄 Aktualizacje w przyszłości

### Jak wydać nową wersję
1. Wprowadź zmiany w kodzie
2. Zaktualizuj `CHANGELOG.md`
3. Zaktualizuj `version` w `manifest.json`
4. Commit i push:
   ```powershell
   git add .
   git commit -m "feat: Dodaj nową funkcję"
   git push
   ```
5. Utwórz tag:
   ```powershell
   git tag v1.1.0
   git push --tags
   ```
6. Utwórz Release na GitHub z tego tagu

---

## 📞 Wsparcie

### Jeśli coś nie działa
1. Sprawdź [QUICKSTART.md](QUICKSTART.md)
2. Sprawdź [PUBLICATION_GUIDE.md](PUBLICATION_GUIDE.md)
3. Sprawdź logi w Home Assistant
4. Utwórz issue na GitHub

### Przydatne komendy
```powershell
# Sprawdź status Git
git status

# Zobacz ostatnie commity
git log --oneline -5

# Zobacz remote
git remote -v

# Sprawdź wersję
git --version

# Sprawdź czy manifest.json jest OK
python -c "import json; print(json.load(open('custom_components/mqtt_link/manifest.json')))"
```

---

## ✅ Finalne sprawdzenie

Przed publikacją upewnij się, że:
- [x] Wszystkie pliki są na miejscu
- [x] Kod został przetestowany
- [x] Dokumentacja jest kompletna
- [x] Linki są poprawne
- [x] Licencja jest OK
- [ ] Twoja nazwa użytkownika jest wszędzie

**Gotowy? Uruchom `.\publish.ps1` i ciesz się! 🎉**

---

## 📊 Post-publikacja

Po opublikowaniu:
- [ ] Sprawdź czy repozytorium jest widoczne
- [ ] Sprawdź czy release został utworzony
- [ ] Sprawdź czy HACS widzi integrację
- [ ] Sprawdź czy można zainstalować
- [ ] Gwiazdka dla własnego repo ⭐

**Gratulacje! Twój dodatek jest publiczny! 🚀**
