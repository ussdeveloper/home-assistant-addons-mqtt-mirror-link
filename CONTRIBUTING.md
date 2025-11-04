# 🤝 Contributing to MQTT Mirror Link

Dziękujemy za zainteresowanie rozwojem MQTT Mirror Link! Każda pomoc jest mile widziana.

## 🐛 Zgłaszanie błędów

### Przed zgłoszeniem
1. Sprawdź czy [issue już istnieje](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/issues)
2. Zaktualizuj do najnowszej wersji
3. Sprawdź logi z poziomem `debug`

### Jak zgłosić
Otwórz [nowe issue](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/issues/new) i podaj:
- **Wersja** MQTT Mirror Link
- **Wersja** Home Assistant
- **Konfiguracja** (bez haseł!)
- **Logi** z `logger: debug`
- **Kroki** do odtworzenia problemu
- **Oczekiwane** zachowanie
- **Rzeczywiste** zachowanie

### Szablon
```markdown
**Wersja MQTT Mirror Link**: 1.0.0
**Wersja Home Assistant**: 2023.11.1

**Konfiguracja**:
- Broker A: localhost:1883
- Broker B: 192.168.1.100:1883
- Bidirectional: Yes
- Topic: homeassistant/#

**Problem**: 
Komunikaty nie są synchronizowane.

**Kroki**:
1. Zainstalowałem integrację
2. Skonfigurowałem brokerów
3. Uruchomiłem HA

**Logi**:
```
[tu wklej logi]
```

**Oczekiwane**: Komunikaty powinny płynąć A→B
**Rzeczywiste**: Brak komunikatów na B
```

---

## 💡 Propozycje nowych funkcji

Masz pomysł na nową funkcję? Super!

### Przed zgłoszeniem
1. Sprawdź czy [nie został już zaproponowany](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/issues?q=is%3Aissue+label%3Aenhancement)
2. Przemyśl czy pasuje do celu projektu

### Jak zgłosić
Otwórz [nowe issue](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/issues/new) z:
- **Opis funkcji**: Co ma robić?
- **Przypadek użycia**: Dlaczego jest potrzebna?
- **Alternatywy**: Czy można to zrobić inaczej?
- **Dodatkowe informacje**: Screenshots, diagramy, etc.

---

## 🔧 Pull Requests

Chcesz dodać kod? Świetnie!

### Proces
1. **Fork** repozytorium
2. **Clone** twojego forka
3. **Branch**: Utwórz nową gałąź
4. **Kod**: Wprowadź zmiany
5. **Test**: Przetestuj dokładnie
6. **Commit**: Z dobrym opisem
7. **Push**: Do swojego forka
8. **PR**: Utwórz Pull Request

### Wymagania
- ✅ Kod zgodny z PEP 8
- ✅ Komentarze po polsku lub angielsku
- ✅ Testy (jeśli możliwe)
- ✅ Dokumentacja zaktualizowana
- ✅ CHANGELOG.md zaktualizowany

### Przykład workflow
```bash
# 1. Fork na GitHub, potem:
git clone https://github.com/TWOJA_NAZWA/home-assistant-addons-mqtt-mirror-link.git
cd home-assistant-addons-mqtt-mirror-link

# 2. Utwórz branch
git checkout -b feature/moja-funkcja

# 3. Wprowadź zmiany
# ... edytuj pliki ...

# 4. Commit
git add .
git commit -m "feat: Dodaj wsparcie dla MQTT 5"

# 5. Push
git push origin feature/moja-funkcja

# 6. Utwórz PR na GitHub
```

### Konwencja commitów
Używamy [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - nowa funkcja
- `fix:` - naprawa błędu
- `docs:` - dokumentacja
- `style:` - formatowanie
- `refactor:` - refaktoryzacja
- `test:` - testy
- `chore:` - pozostałe

**Przykłady**:
```
feat: Dodaj wsparcie dla QoS filtering
fix: Napraw pętlę przy bidirectional sync
docs: Aktualizuj README z przykładami
```

---

## 🧪 Testowanie

### Lokalne testowanie
1. Skopiuj `custom_components/mqtt_link` do HA
2. Zrestartuj HA
3. Skonfiguruj integrację
4. Sprawdź logi: `logger: debug`

### Środowisko testowe
```yaml
# configuration.yaml
logger:
  default: info
  logs:
    custom_components.mqtt_link: debug
```

### Checklist przed PR
- [ ] Kod działa lokalnie
- [ ] Żadne błędy w logach
- [ ] Dokumentacja zaktualizowana
- [ ] CHANGELOG.md zaktualizowany
- [ ] Kod sformatowany (PEP 8)
- [ ] Commity zgodne z konwencją

---

## 📝 Dokumentacja

### Pliki do aktualizacji
- `README.md` - główna dokumentacja
- `info.md` - opis dla HACS
- `EXAMPLES.md` - przykłady
- `CHANGELOG.md` - historia zmian
- `strings.json` - tłumaczenia PL
- `translations/en.json` - tłumaczenia EN

### Tłumaczenia
Dodając nowe stringi, zaktualizuj:
1. `strings.json` (PL)
2. `translations/en.json` (EN)

---

## 🎨 Styl kodu

### Python
- PEP 8
- Linijka max 88 znaków (Black formatter)
- Type hints gdzie możliwe
- Docstringi po polsku lub angielsku

### Przykład
```python
def sync_message(self, topic: str, payload: bytes, qos: int) -> None:
    """Synchronizuj wiadomość MQTT między brokerami.
    
    Args:
        topic: Temat MQTT
        payload: Zawartość wiadomości
        qos: Quality of Service (0-2)
    """
    try:
        self.client_b.publish(topic, payload, qos=qos)
    except Exception as e:
        _LOGGER.error(f"Błąd synchronizacji: {e}")
```

---

## 🏗️ Struktura projektu

```
mqtt_link/
├── custom_components/
│   └── mqtt_link/
│       ├── __init__.py          # Główna logika
│       ├── config_flow.py       # UI konfiguracji
│       ├── manifest.json        # Metadane
│       ├── strings.json         # Tłumaczenia PL
│       └── translations/
│           └── en.json          # Tłumaczenia EN
├── .github/
│   └── workflows/
│       ├── validate.yml         # CI walidacja
│       └── release.yml          # Release automation
├── README.md                    # Główna dokumentacja
├── EXAMPLES.md                  # Przykłady użycia
├── QUICKSTART.md               # Szybki start
└── CHANGELOG.md                # Historia zmian
```

---

## 📋 Roadmap

Przyszłe funkcje (pomoc mile widziana!):
- [ ] Wsparcie dla MQTT 5
- [ ] QoS filtering
- [ ] Topic transformations
- [ ] Payload filtering/modification
- [ ] Multiple brokers (więcej niż 2)
- [ ] Statistics/monitoring
- [ ] Web UI dla diagnostyki
- [ ] Docker standalone version

---

## 🙏 Dziękujemy!

Każdy wkład się liczy:
- 🐛 Zgłaszanie błędów
- 💡 Propozycje funkcji
- 📖 Poprawki w dokumentacji
- 🔧 Pull requesty
- ⭐ Gwiazdki na GitHub
- 💬 Pomoc innym użytkownikom

## 📞 Kontakt

- **Issues**: [GitHub Issues](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/discussions)

---

**Wesołego kodowania!** 🚀
