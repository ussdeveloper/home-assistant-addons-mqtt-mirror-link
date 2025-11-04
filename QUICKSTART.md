# 🚀 Szybki Start - MQTT Mirror Link

## 📋 Spis treści
1. [Publikacja na GitHub](#1-publikacja-na-github)
2. [Instalacja w Home Assistant](#2-instalacja-w-home-assistant)
3. [Konfiguracja](#3-konfiguracja)

---

## 1️⃣ Publikacja na GitHub

### Krok 1: Utwórz repozytorium
1. Idź na https://github.com/new
2. Nazwa: `home-assistant-addons-mqtt-mirror-link`
3. Public, **bez** README/LICENSE
4. Kliknij **Create repository**

### Krok 2: Wypchnij kod (wybierz jedną metodę)

#### Metoda A: Automatyczna (łatwiejsza) ✨
```powershell
cd "c:\Users\sulaco\Desktop\HomeAssistant MQTT LINK"
.\publish.ps1
```

#### Metoda B: Manualna
```powershell
cd "c:\Users\sulaco\Desktop\HomeAssistant MQTT LINK"
git init
git add .
git commit -m "Initial commit: MQTT Mirror Link v1.0.0"
git branch -M main
git remote add origin https://github.com/TWOJA_NAZWA/home-assistant-addons-mqtt-mirror-link.git
git push -u origin main
```

### Krok 3: Utwórz Release
1. Na GitHub: **Releases** → **Create a new release**
2. Tag: `v1.0.0`
3. Title: `v1.0.0 - Initial Release 🎉`
4. Publish!

---

## 2️⃣ Instalacja w Home Assistant

### Dodaj repozytorium do HACS
1. Otwórz **HACS** → **Integrations**
2. Menu **⋮** → **Custom repositories**
3. URL: `https://github.com/TWOJA_NAZWA/home-assistant-addons-mqtt-mirror-link`
4. Kategoria: **Integration**
5. Kliknij **Add**

### Pobierz integrację
1. Znajdź **MQTT Mirror Link** w HACS
2. Kliknij **Download**
3. **Zrestartuj** Home Assistant

---

## 3️⃣ Konfiguracja

### Dodaj integrację
1. **Ustawienia** → **Urządzenia i usługi**
2. **+ DODAJ INTEGRACJĘ**
3. Wyszukaj **MQTT Mirror Link**

### Skonfiguruj Broker A (lokalny)
```
Host:       localhost
Port:       1883
Username:   (opcjonalnie)
Password:   (opcjonalnie)
Topic:      #
```

### Skonfiguruj Broker B (zdalny)
```
Host:       192.168.1.100    (IP drugiego HA)
Port:       1883
Username:   (opcjonalnie)
Password:   (opcjonalnie)
Topic:      #
Bidirect:   ✓ TAK
```

### Gotowe! 🎉

Wszystkie komunikaty MQTT z obu Home Assistant będą teraz synchronizowane!

---

## 🔍 Sprawdzanie czy działa

### 1. Sprawdź logi
```yaml
# configuration.yaml
logger:
  logs:
    custom_components.mqtt_link: debug
```

### 2. Testuj
- Zmień stan urządzenia na HA-A
- Sprawdź czy pojawił się na HA-B
- Działa? Super! 🎊

---

## 🆘 Pomoc

- 📖 Pełna dokumentacja: [README.md](README.md)
- 📋 Szczegóły publikacji: [PUBLICATION_GUIDE.md](PUBLICATION_GUIDE.md)
- 🐛 Problemy: [GitHub Issues](https://github.com/TWOJA_NAZWA/home-assistant-addons-mqtt-mirror-link/issues)

---

## 📝 Notatki

### Ważne adresy (zmień TWOJA_NAZWA!)
- Repozytorium: `https://github.com/TWOJA_NAZWA/home-assistant-addons-mqtt-mirror-link`
- URL do HACS: to samo ↑

### Typowe problemy
- **Git nie znaleziony**: zainstaluj z https://git-scm.com
- **Push error**: sprawdź czy repozytorium istnieje i masz dostęp
- **Nie widać w HACS**: sprawdź czy release został utworzony

### Następna aktualizacja
```powershell
git add .
git commit -m "Opis zmian"
git push
git tag v1.1.0
git push --tags
# Potem utwórz Release na GitHub
```

---

**Gotowe w 3 kroki: Publikuj → Instaluj → Konfiguruj** ✨
