# 🧪 Testy MQTT Mirror Link

Przewodnik testowania i debugowania MQTT Mirror Link.

## 📋 Wymagania

### Narzędzia MQTT

#### Windows
```powershell
# Mosquitto (zawiera mosquitto_pub i mosquitto_sub)
choco install mosquitto
# lub pobierz z: https://mosquitto.org/download/
```

#### Linux/Mac
```bash
sudo apt-get install mosquitto-clients  # Debian/Ubuntu
brew install mosquitto                  # macOS
```

### Alternatywy
- **MQTT Explorer** (GUI): https://mqtt-explorer.com/
- **MQTT.fx** (GUI): https://mqttfx.jensd.de/
- **Python paho-mqtt**:
  ```bash
  pip install paho-mqtt
  ```

---

## 🔍 Sprawdzanie statusu

### 1. Status integracji w HA
```
Ustawienia → Urządzenia i usługi → MQTT Mirror Link
```

Powinno być: ✅ Configured

### 2. Logi Home Assistant
```yaml
# configuration.yaml
logger:
  default: info
  logs:
    custom_components.mqtt_link: debug
```

Sprawdź logi:
```
Ustawienia → System → Logi → Filtr: mqtt_link
```

Szukaj:
- `Połączono z brokerem A`
- `Połączono z brokerem B`
- `A->B: topic = payload`
- `B->A: topic = payload`

---

## 🧪 Testy podstawowe

### Test 1: Sprawdź połączenie z brokerem

#### Broker A (lokalny)
```bash
# Wyślij testową wiadomość
mosquitto_pub -h localhost -p 1883 -t test/mirror -m "Hello from A"

# Odbierz na tym samym brokerze (powinno zadziałać zawsze)
mosquitto_sub -h localhost -p 1883 -t test/mirror -C 1
```

#### Broker B (zdalny)
```bash
# Wyślij testową wiadomość
mosquitto_pub -h 192.168.1.100 -p 1883 -t test/mirror -m "Hello from B"

# Odbierz
mosquitto_sub -h 192.168.1.100 -p 1883 -t test/mirror -C 1
```

### Test 2: Synchronizacja A→B

```bash
# Terminal 1: Nasłuchuj na B
mosquitto_sub -h 192.168.1.100 -p 1883 -t test/mirror -v

# Terminal 2: Wyślij z A
mosquitto_pub -h localhost -p 1883 -t test/mirror -m "Test A to B"
```

**Oczekiwany wynik**: Wiadomość pojawi się w Terminal 1

### Test 3: Synchronizacja B→A (jeśli bidirectional)

```bash
# Terminal 1: Nasłuchuj na A
mosquitto_sub -h localhost -p 1883 -t test/mirror -v

# Terminal 2: Wyślij z B
mosquitto_pub -h 192.168.1.100 -p 1883 -t test/mirror -m "Test B to A"
```

**Oczekiwany wynik**: Wiadomość pojawi się w Terminal 1

### Test 4: Wszystkie komunikaty (#)

```bash
# Terminal 1: Nasłuchuj wszystkiego na B
mosquitto_sub -h 192.168.1.100 -p 1883 -t '#' -v

# Terminal 2: Wyślij różne tematy z A
mosquitto_pub -h localhost -p 1883 -t sensors/temp -m "22.5"
mosquitto_pub -h localhost -p 1883 -t lights/living/state -m "ON"
mosquitto_pub -h localhost -p 1883 -t homeassistant/sensor/test/state -m '{"value": 123}'
```

**Oczekiwany wynik**: Wszystkie wiadomości pojawiają się na B

---

## 🔧 Testy z uwierzytelnianiem

### Jeśli MQTT wymaga loginu

```bash
# Dodaj -u username -P password
mosquitto_pub -h 192.168.1.100 -p 1883 -u mqttuser -P mqttpass -t test/auth -m "Authenticated"

mosquitto_sub -h 192.168.1.100 -p 1883 -u mqttuser -P mqttpass -t test/auth -v
```

---

## 🎯 Testy filtrowania tematów

### Filtr: homeassistant/#

Powinny przejść:
```bash
mosquitto_pub -h localhost -t homeassistant/sensor/test/state -m "OK"  # ✅
mosquitto_pub -h localhost -t homeassistant/light/lamp/command -m "ON"  # ✅
```

Nie powinny przejść:
```bash
mosquitto_pub -h localhost -t zigbee2mqtt/sensor/temp -m "22"  # ❌
mosquitto_pub -h localhost -t custom/topic -m "test"  # ❌
```

### Filtr: homeassistant/sensor/+/state

Powinny przejść:
```bash
mosquitto_pub -h localhost -t homeassistant/sensor/temp/state -m "22"  # ✅
mosquitto_pub -h localhost -t homeassistant/sensor/humidity/state -m "60"  # ✅
```

Nie powinny przejść:
```bash
mosquitto_pub -h localhost -t homeassistant/light/lamp/state -m "ON"  # ❌
mosquitto_pub -h localhost -t homeassistant/sensor/temp/config -m "{}"  # ❌
```

---

## 📊 Testy QoS

### QoS 0 (co najwyżej raz)
```bash
mosquitto_pub -h localhost -t test/qos0 -m "QoS 0" -q 0
```

### QoS 1 (co najmniej raz)
```bash
mosquitto_pub -h localhost -t test/qos1 -m "QoS 1" -q 1
```

### QoS 2 (dokładnie raz)
```bash
mosquitto_pub -h localhost -t test/qos2 -m "QoS 2" -q 2
```

**Sprawdź logi**: MQTT Mirror Link powinien zachować oryginalny QoS.

---

## 🔁 Testy retain

### Wiadomość z retain
```bash
# Wyślij z retain
mosquitto_pub -h localhost -t test/retain -m "Retained message" -r

# Nowy subscriber powinien od razu otrzymać wiadomość
mosquitto_sub -h 192.168.1.100 -t test/retain -C 1
```

**Oczekiwany wynik**: Wiadomość jest od razu dostępna dla nowych subskrybentów.

### Wyczyść retain
```bash
# Wyślij pustą wiadomość z retain
mosquitto_pub -h localhost -t test/retain -n -r
```

---

## ⚠️ Testy problemów

### Test 1: Pętla komunikatów

**Scenariusz**: Bidirectional sync z tym samym tematem

```bash
# Terminal 1: Loguj wszystko na A
mosquitto_sub -h localhost -t '#' -v

# Terminal 2: Loguj wszystko na B
mosquitto_sub -h 192.168.1.100 -t '#' -v

# Terminal 3: Wyślij wiadomość
mosquitto_pub -h localhost -t test/loop -m "Loop test"
```

**Sprawdź**: Czy wiadomość się multiplikuje? (jeśli tak = pętla!)

**Rozwiązanie**: Użyj różnych tematów lub wyłącz bidirectional.

### Test 2: Duże obciążenie

```bash
# Wyślij 1000 wiadomości szybko
for i in {1..1000}; do
  mosquitto_pub -h localhost -t test/load -m "Message $i"
done
```

**Sprawdź**:
- Czy wszystkie dotarły do B?
- Czy są lagi w logach?
- CPU/RAM usage

### Test 3: Utrata połączenia

```bash
# 1. Uruchom subscriber na B
mosquitto_sub -h 192.168.1.100 -t test/reconnect -v

# 2. Wyłącz broker B (lub sieć)

# 3. Wyślij wiadomości z A
mosquitto_pub -h localhost -t test/reconnect -m "Before disconnect"

# 4. Włącz broker B z powrotem

# 5. Wyślij ponownie
mosquitto_pub -h localhost -t test/reconnect -m "After reconnect"
```

**Oczekiwany wynik**: Po reconnect, nowe wiadomości są synchronizowane.

---

## 🐍 Skrypt testowy Python

```python
#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import time

# Konfiguracja
BROKER_A = "localhost"
BROKER_B = "192.168.1.100"
PORT = 1883
TOPIC = "test/python"

def on_message_a(client, userdata, msg):
    print(f"[A] {msg.topic}: {msg.payload.decode()}")

def on_message_b(client, userdata, msg):
    print(f"[B] {msg.topic}: {msg.payload.decode()}")

# Klienci
client_a = mqtt.Client("test_a")
client_a.on_message = on_message_a
client_a.connect(BROKER_A, PORT)
client_a.subscribe(TOPIC)
client_a.loop_start()

client_b = mqtt.Client("test_b")
client_b.on_message = on_message_b
client_b.connect(BROKER_B, PORT)
client_b.subscribe(TOPIC)
client_b.loop_start()

# Test
print("Wysyłam z A do B...")
client_a.publish(TOPIC, "Hello from A")
time.sleep(1)

print("Wysyłam z B do A...")
client_b.publish(TOPIC, "Hello from B")
time.sleep(1)

# Cleanup
client_a.loop_stop()
client_b.loop_stop()
print("Test zakończony!")
```

Zapisz jako `test_mqtt.py` i uruchom:
```bash
python test_mqtt.py
```

---

## 📈 Monitoring długoterminowy

### MQTT Explorer
1. Pobierz: https://mqtt-explorer.com/
2. Podłącz do obu brokerów
3. Obserwuj komunikaty w czasie rzeczywistym
4. Sprawdź statystyki

### Home Assistant Statistics
```yaml
# configuration.yaml
mqtt:
  sensor:
    - name: "MQTT Link A Messages"
      state_topic: "$SYS/broker/messages/sent"
      
    - name: "MQTT Link B Messages"
      state_topic: "$SYS/broker/messages/received"
```

---

## 🐛 Debug checklist

Jeśli coś nie działa:

- [ ] Broker A jest uruchomiony
- [ ] Broker B jest uruchomiony
- [ ] Porty są otwarte w firewall
- [ ] Dane logowania są poprawne
- [ ] Tematy są poprawne (bez typo)
- [ ] MQTT Mirror Link jest uruchomiony
- [ ] Logi debug są włączone
- [ ] Konfiguracja jest zapisana
- [ ] Home Assistant został zrestartowany po instalacji

---

## 📞 Pomoc

Jeśli testy nie przechodzą:
1. Sprawdź logi: `logger: debug`
2. Zobacz [EXAMPLES.md](EXAMPLES.md)
3. Utwórz issue z wynikami testów

**Powodzenia w testowaniu!** 🧪
