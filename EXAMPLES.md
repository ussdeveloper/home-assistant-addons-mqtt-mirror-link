# 📚 Przykłady konfiguracji MQTT Mirror Link

## 🎯 Scenariusze użycia

### 1. Pełna synchronizacja dwóch Home Assistant

**Przypadek użycia**: Masz dwie instancje HA (np. główna i testowa) i chcesz, aby wszystko było zsynchronizowane.

**Konfiguracja:**
```
Broker A (localhost):
  Host: localhost
  Port: 1883
  Topic: #
  
Broker B (192.168.1.100):
  Host: 192.168.1.100
  Port: 1883
  Topic: #
  Bidirectional: ✓ TAK
```

**Efekt**: Wszystkie komunikaty MQTT płyną w obie strony.

---

### 2. Backup jednokierunkowy

**Przypadek użycia**: Chcesz mieć kopię zapasową wszystkich stanów na drugim HA, ale bez wpływu zwrotnego.

**Konfiguracja:**
```
Broker A (główny):
  Host: localhost
  Port: 1883
  Topic: #
  
Broker B (backup):
  Host: 192.168.1.200
  Port: 1883
  Topic: #
  Bidirectional: ✗ NIE
```

**Efekt**: A → B, ale nie B → A

---

### 3. Tylko urządzenia Home Assistant

**Przypadek użycia**: Chcesz synchronizować tylko urządzenia wykrywane przez HA, bez innych tematów MQTT.

**Konfiguracja:**
```
Broker A:
  Topic: homeassistant/#
  
Broker B:
  Topic: homeassistant/#
  Bidirectional: ✓ TAK
```

**Efekt**: Tylko tematy `homeassistant/*` są synchronizowane.

---

### 4. Synchronizacja wybranych urządzeń

**Przypadek użycia**: Tylko sensory z salonu.

**Konfiguracja:**
```
Broker A:
  Topic: homeassistant/sensor/salon_+/+
  
Broker B:
  Topic: homeassistant/sensor/salon_+/+
  Bidirectional: ✓ TAK
```

**Efekt**: Tylko sensory z salonu są synchronizowane.

---

### 5. Zdalna lokalizacja (przez Internet)

**Przypadek użycia**: Synchronizacja między dwoma domami.

**Konfiguracja:**
```
Broker A (Dom 1):
  Host: localhost
  Port: 1883
  Username: user1
  Password: pass1
  Topic: #
  
Broker B (Dom 2 - przez VPN/Tailscale):
  Host: 10.0.0.5
  Port: 1883
  Username: user2
  Password: pass2
  Topic: #
  Bidirectional: ✓ TAK
```

**Wymagania**:
- VPN lub Tailscale
- Port 1883 otwarty w firewall
- Uwierzytelnianie MQTT włączone

---

### 6. Multi-master (więcej niż 2 HA)

**Przypadek użycia**: 3 instancje HA (A, B, C)

**Rozwiązanie**: Zainstaluj MQTT Mirror Link na każdej instancji:

**Na HA-A:**
```
Broker A: localhost
Broker B: HA-B (192.168.1.100)
Bidirectional: ✓
```

**Na HA-B:**
```
Broker A: localhost
Broker B: HA-C (192.168.1.101)
Bidirectional: ✓
```

**Efekt**: A ↔ B ↔ C (wszystkie zsynchronizowane)

⚠️ **Uwaga**: Może wystąpić pętla! Użyj różnych tematów lub wyłącz bidirectional.

---

### 7. Filtrowanie po QoS

**Przypadek użycia**: Tylko ważne komunikaty (QoS 1+)

⚠️ **Uwaga**: Obecnie nie jest wspierane przez integrację. Wszystkie komunikaty są przekazywane z zachowaniem oryginalnego QoS.

**Workaround**: Użyj filtrowania tematów.

---

### 8. Hub-and-Spoke (gwiazda)

**Przypadek użycia**: Jeden centralny HA (hub) i kilka satelitów.

**Architektura:**
```
    HA-Hub (central)
      /  |  \
    HA1 HA2 HA3
```

**Konfiguracja**: Każdy satelita ma MQTT Mirror Link skierowany do hub.

**Na HA1, HA2, HA3:**
```
Broker A: localhost
Broker B: HA-Hub (192.168.1.10)
Bidirectional: ✓
```

**Efekt**: Wszystko przechodzi przez hub.

---

### 9. Izolacja namespace

**Przypadek użycia**: Nie chcesz kolizji nazw między HA-A i HA-B.

**Rozwiązanie**: Użyj prefiksów w tematach MQTT.

**Configuration.yaml na HA-A:**
```yaml
mqtt:
  discovery_prefix: homeassistant_a
```

**Configuration.yaml na HA-B:**
```yaml
mqtt:
  discovery_prefix: homeassistant_b
```

**MQTT Mirror Link:**
```
Broker A:
  Topic: homeassistant_a/#
  
Broker B:
  Topic: homeassistant_b/#
  Bidirectional: ✓
```

**Efekt**: Urządzenia mają różne prefiksy i nie powodują konfliktów.

---

### 10. Monitorowanie z Grafana

**Przypadek użycia**: Zbieraj wszystkie metryki MQTT w jednym miejscu.

**Konfiguracja:**
```
Broker A (HA): localhost
Broker B (Grafana MQTT): 192.168.1.50:1883
Topic: homeassistant/sensor/+/state
Bidirectional: ✗ NIE
```

**Efekt**: Wszystkie stany sensorów idą do Grafany, ale nic nie wraca.

---

## 🔧 Zaawansowane porady

### Wildcard w tematach
- `#` = wszystko (wielopoziomowy wildcard)
- `+` = jeden poziom (jednopoziomowy wildcard)

**Przykłady:**
- `homeassistant/#` = wszystkie tematy HA
- `homeassistant/+/salon/#` = wszystkie urządzenia w salonie
- `homeassistant/sensor/+/state` = wszystkie stany sensorów

### QoS
- QoS 0: co najwyżej raz (brak gwarancji)
- QoS 1: co najmniej raz (potwierdzona doręczenie)
- QoS 2: dokładnie raz (najwolniejsze)

**Zachowanie**: MQTT Mirror Link zachowuje oryginalny QoS każdego komunikatu.

### Retain flag
**Zachowanie**: MQTT Mirror Link zachowuje oryginalny retain flag.

- `retain=true`: Ostatnia wiadomość jest zapisywana przez brokera
- `retain=false`: Wiadomość nie jest zapisywana

---

## ⚠️ Problemy i rozwiązania

### Problem: Pętla komunikatów

**Objawy**: Duplikaty, rosnąca liczba wiadomości

**Rozwiązanie**:
1. Użyj różnych tematów dla A i B
2. Wyłącz bidirectional
3. Dodaj filtrowanie

### Problem: Zbyt duże obciążenie

**Objawy**: Wolny MQTT, duże użycie CPU/sieci

**Rozwiązanie**:
1. Ogranicz tematy (nie używaj `#`)
2. Użyj QoS 0
3. Wyłącz retain gdzie niepotrzebny

### Problem: Nie synchronizuje się

**Objawy**: Brak komunikatów na drugiej stronie

**Rozwiązanie**:
1. Sprawdź logi (logger: debug)
2. Sprawdź firewall
3. Sprawdź uprawnienia użytkownika MQTT
4. Sprawdź czy tematy się zgadzają

---

## 📖 Więcej informacji

- [README.md](README.md) - Pełna dokumentacja
- [QUICKSTART.md](QUICKSTART.md) - Szybki start
- [PUBLICATION_GUIDE.md](PUBLICATION_GUIDE.md) - Publikacja na GitHub

---

**Pytania? Utwórz issue na GitHub!** 🐛
