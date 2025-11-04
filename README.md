# MQTT Mirror Link - Home Assistant Add-on

[![GitHub Release](https://img.shields.io/github/release/ussdeveloper/home-assistant-addons-mqtt-mirror-link.svg)](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/releases)
[![License](https://img.shields.io/github/license/ussdeveloper/home-assistant-addons-mqtt-mirror-link.svg)](LICENSE)

**Wirtualny, jednolity broker MQTT dla Home Assistant - łącz wiele upstream brokerów w jedno!**

## 🎯 Co to robi?

MQTT Mirror Link to Home Assistant Add-on, który tworzy **wirtualny, jednolity broker MQTT** (lokalny endpoint dla Home Assistant). Addon wewnętrznie łączy się z wieloma upstream brokerami MQTT, tworząc jednolitą przestrzeń komunikatów.

### Architektura v2.0

```
Home Assistant
      ↕
Local Broker (localhost:1883)  ← Ten addon
      ↕              ↕
Upstream A     Upstream B
(broker 1)     (broker 2)
```

**Jak to działa:**
- Home Assistant łączy się tylko do lokalnego brokera (ten addon)
- Addon łączy się do wielu upstream brokerów (dowolna liczba)
- Wszystkie komunikaty są automatycznie synchronizowane
- Wbudowana detekcja pętli (LRU cache + MQTT v5 origin tagging)

## ✨ Funkcje

- ✅ **Wirtualny jednolity broker** - jeden endpoint dla Home Assistant
- ✅ **Wiele upstream brokerów** - nieograniczona liczba połączeń
- ✅ **Automatyczna detekcja pętli** - sha1 hashing + LRU cache (50k wiadomości, 30s TTL)
- ✅ **MQTT v5 origin tagging** - user properties do śledzenia źródła
- ✅ **Fan-in/fan-out routing** - lokalny→wszystkie upstreamy, upstream A→lokalny+upstream B
- ✅ **Filtrowanie $SYS/#** - wyklucza systemowe topiki brokerów
- ✅ **Uwierzytelnianie** - pełne wsparcie dla username/password
- ✅ **Automatyczne reconnect** - po utracie połączenia
- ✅ **Node.js 20 + TypeScript** - nowoczesny stack technologiczny

## 📦 Instalacja

1. W Home Assistant przejdź do **Settings** → **Add-ons**
2. Kliknij **Add-on Store** (prawy dolny róg)
3. Menu **⋮** (prawy górny róg) → **Repositories**
4. Dodaj URL: `https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link`
5. Znajdź **MQTT Mirror Link** i kliknij **INSTALL**
6. Przejdź do zakładki **Configuration**
7. Skonfiguruj (zobacz przykłady poniżej)
8. Uruchom addon (zakładka **Info** → **START**)

## ⚙️ Konfiguracja

### Parametry lokalne (Local Broker)

- **listen.host** - IP gdzie słucha lokalny broker (domyślnie: `0.0.0.0`)
- **listen.port** - Port lokalnego brokera (domyślnie: `1883`)

### Parametry upstream brokerów

Tablica `upstreams` zawiera listę brokerów do połączenia:

```yaml
upstreams:
  - host: "192.168.1.100"
    port: 1883
    username: "mqtt_user"
    password: "mqtt_pass"
    topics: ["#"]
    client_id: "ha-mqtt-unifier-upstream-1"
    
  - host: "192.168.1.200"
    port: 1883
    username: "mqtt_user2"
    password: "mqtt_pass2"
    topics: ["homeassistant/#", "zigbee2mqtt/#"]
    client_id: "ha-mqtt-unifier-upstream-2"
```

**Każdy upstream broker:**
- `host` - adres IP lub hostname
- `port` - port MQTT (domyślnie: 1883)
- `username` - nazwa użytkownika (opcjonalne)
- `password` - hasło (opcjonalne)
- `topics` - lista tematów do subskrypcji (domyślnie: ["#"])
- `client_id` - unikalny ID klienta MQTT

### Dodatkowe parametry

- **discovery_prefix** - prefiks Home Assistant discovery (domyślnie: `homeassistant`)
- **retain_cache_ttl_sec** - TTL cache dla wiadomości z retain (domyślnie: 30)
- **max_lru** - maksymalna wielkość LRU cache (domyślnie: 50000)

## 📋 Przykłady konfiguracji

### Przykład 1: Dwa brokery MQTT - pełna synchronizacja

```yaml
upstreams:
  - host: "192.168.1.100"
    port: 1883
    username: "mqtt"
    password: "secret1"
    topics: ["#"]
    client_id: "ha-unifier-broker1"
    
  - host: "192.168.1.200"
    port: 1883
    username: "mqtt"
    password: "secret2"
    topics: ["#"]
    client_id: "ha-unifier-broker2"
```

### Przykład 2: Tylko topiki Home Assistant i Zigbee2MQTT

```yaml
upstreams:
  - host: "192.168.1.100"
    port: 1883
    topics: 
      - "homeassistant/#"
      - "zigbee2mqtt/#"
    client_id: "ha-unifier-filtered"
```

### Przykład 3: Trzy brokery - różne porty

```yaml
upstreams:
  - host: "mqtt.home.local"
    port: 1883
    topics: ["#"]
    
  - host: "mqtt.cloud.com"
    port: 8883
    username: "cloud_user"
    password: "cloud_pass"
    topics: ["cloud/#"]
    
  - host: "192.168.1.150"
    port: 1884
    topics: ["sensors/#"]
```

### Konfiguracja Home Assistant

Po uruchomieniu addonu, skonfiguruj Home Assistant aby łączył się do lokalnego brokera:

**configuration.yaml:**
```yaml
mqtt:
  broker: localhost
  port: 1883
  # username/password jeśli wymagane przez upstream brokery
```

## 🔧 Rozwiązywanie problemów

### Sprawdź logi addonu

W Home Assistant:
1. Przejdź do **Settings** → **Add-ons** → **MQTT Mirror Link**
2. Zakładka **Log** - sprawdź błędy połączeń z upstream brokerami

### Typowe problemy

**Problem**: Addon nie startuje
- Sprawdź logi addonu
- Upewnij się, że format konfiguracji YAML jest poprawny
- Sprawdź czy port 1883 nie jest już zajęty

**Problem**: Home Assistant nie łączy się z lokalnym brokerem
- Upewnij się że addon jest uruchomiony (status: **Running**)
- Sprawdź `configuration.yaml` - broker powinien być `localhost:1883`
- Zrestartuj Home Assistant po zmianie konfiguracji MQTT

**Problem**: Brak synchronizacji z upstream brokerami
- Sprawdź dane logowania (username/password)
- Sprawdź dostępność sieciową (ping do upstream brokerów)
- Sprawdź firewall i uprawnienia użytkownika MQTT
- Sprawdź logi addonu - zobaczysz błędy połączeń

**Problem**: Duplikaty wiadomości
- Nie powinno się zdarzać - addon ma wbudowaną detekcję pętli
- Jeśli występuje, zwiększ `retain_cache_ttl_sec`
- Sprawdź logi - zobaczysz "Ignoring duplicate message" gdy działa detekcja

## 📝 Changelog

Zobacz [CHANGELOG.md](CHANGELOG.md) dla pełnej historii zmian.

**Najnowsza wersja: v2.0.1**
- Kompletny redesign architektury (virtual unified broker)
- Node.js 20 + TypeScript + Aedes + mqtt.js
- LRU cache deduplication + MQTT v5 origin tagging
- Nieograniczona liczba upstream brokerów

## 🛠️ Stack Technologiczny

- **Node.js 20** - runtime environment
- **TypeScript 5.6** - type-safe development
- **Aedes 0.51.3** - lightweight MQTT broker library
- **mqtt.js 5.10.1** - MQTT v5 client library
- **lru-cache 10.4.3** - deduplikacja wiadomości
- **Alpine Linux 3.20** - Docker base image

## 📄 Licencja

MIT License - zobacz [LICENSE](LICENSE)

## 🤝 Wsparcie

- 🐛 **Zgłoś problem**: [GitHub Issues](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/issues)
- 💬 **Dyskusja**: [GitHub Discussions](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link/discussions)

## ⭐ Podoba Ci się?

Zostaw ⭐ na [GitHub](https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link)!
