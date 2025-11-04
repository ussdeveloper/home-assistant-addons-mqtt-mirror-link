"""MQTT Link Integration - synchronizacja komunikatów między dwoma brokerami MQTT."""
import logging
import asyncio
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
import paho.mqtt.client as mqtt

_LOGGER = logging.getLogger(__name__)

DOMAIN = "mqtt_link"


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Ustaw integrację MQTT Link."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Ustaw MQTT Link z config entry."""
    mqtt_bridge = MQTTBridge(hass, entry)
    
    hass.data[DOMAIN][entry.entry_id] = mqtt_bridge
    
    # Uruchom bridge
    await hass.async_add_executor_job(mqtt_bridge.start)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Usuń MQTT Link config entry."""
    mqtt_bridge = hass.data[DOMAIN].pop(entry.entry_id)
    await hass.async_add_executor_job(mqtt_bridge.stop)
    return True


class MQTTBridge:
    """Klasa obsługująca synchronizację między dwoma brokerami MQTT."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Inicjalizuj MQTT Bridge."""
        self.hass = hass
        self.entry = entry
        
        # Pobierz konfigurację
        config = entry.data
        
        # Konfiguracja brokera A (lokalny Home Assistant)
        self.broker_a_host = config.get("broker_a_host", "localhost")
        self.broker_a_port = config.get("broker_a_port", 1883)
        self.broker_a_username = config.get("broker_a_username")
        self.broker_a_password = config.get("broker_a_password")
        self.broker_a_topic = config.get("broker_a_topic", "#")
        
        # Konfiguracja brokera B (zdalny Home Assistant)
        self.broker_b_host = config["broker_b_host"]
        self.broker_b_port = config.get("broker_b_port", 1883)
        self.broker_b_username = config.get("broker_b_username")
        self.broker_b_password = config.get("broker_b_password")
        self.broker_b_topic = config.get("broker_b_topic", "#")
        
        # Opcje synchronizacji
        self.bidirectional = config.get("bidirectional", True)
        
        # Klienci MQTT
        self.client_a = None
        self.client_b = None
        
        # Flaga działania
        self.running = False

    def start(self) -> None:
        """Uruchom mostek MQTT."""
        _LOGGER.info("Uruchamianie MQTT Link...")
        
        # Utwórz klientów MQTT
        self.client_a = mqtt.Client(client_id="mqtt_link_a")
        self.client_b = mqtt.Client(client_id="mqtt_link_b")
        
        # Ustaw callbacks dla klienta A
        self.client_a.on_connect = self._on_connect_a
        self.client_a.on_message = self._on_message_a
        self.client_a.on_disconnect = self._on_disconnect_a
        
        # Ustaw callbacks dla klienta B
        self.client_b.on_connect = self._on_connect_b
        self.client_b.on_message = self._on_message_b
        self.client_b.on_disconnect = self._on_disconnect_b
        
        # Ustaw uwierzytelnianie dla brokera A
        if self.broker_a_username:
            self.client_a.username_pw_set(
                self.broker_a_username, 
                self.broker_a_password
            )
        
        # Ustaw uwierzytelnianie dla brokera B
        if self.broker_b_username:
            self.client_b.username_pw_set(
                self.broker_b_username, 
                self.broker_b_password
            )
        
        try:
            # Połącz z brokerem A
            _LOGGER.info(f"Łączenie z brokerem A: {self.broker_a_host}:{self.broker_a_port}")
            self.client_a.connect(self.broker_a_host, self.broker_a_port, 60)
            
            # Połącz z brokerem B
            _LOGGER.info(f"Łączenie z brokerem B: {self.broker_b_host}:{self.broker_b_port}")
            self.client_b.connect(self.broker_b_host, self.broker_b_port, 60)
            
            # Uruchom pętle sieciowe
            self.client_a.loop_start()
            self.client_b.loop_start()
            
            self.running = True
            _LOGGER.info("MQTT Link uruchomiony pomyślnie")
            
        except Exception as e:
            _LOGGER.error(f"Błąd podczas uruchamiania MQTT Link: {e}")
            self.stop()

    def stop(self) -> None:
        """Zatrzymaj mostek MQTT."""
        _LOGGER.info("Zatrzymywanie MQTT Link...")
        self.running = False
        
        if self.client_a:
            self.client_a.loop_stop()
            self.client_a.disconnect()
        
        if self.client_b:
            self.client_b.loop_stop()
            self.client_b.disconnect()
        
        _LOGGER.info("MQTT Link zatrzymany")

    def _on_connect_a(self, client, userdata, flags, rc):
        """Callback wywoływany po połączeniu z brokerem A."""
        if rc == 0:
            _LOGGER.info(f"Połączono z brokerem A, subskrybowanie: {self.broker_a_topic}")
            client.subscribe(self.broker_a_topic)
        else:
            _LOGGER.error(f"Nie udało się połączyć z brokerem A, kod: {rc}")

    def _on_connect_b(self, client, userdata, flags, rc):
        """Callback wywoływany po połączeniu z brokerem B."""
        if rc == 0:
            _LOGGER.info(f"Połączono z brokerem B, subskrybowanie: {self.broker_b_topic}")
            if self.bidirectional:
                client.subscribe(self.broker_b_topic)
        else:
            _LOGGER.error(f"Nie udało się połączyć z brokerem B, kod: {rc}")

    def _on_message_a(self, client, userdata, msg):
        """Callback wywoływany po otrzymaniu wiadomości z brokera A."""
        if not self.running:
            return
            
        try:
            # Prześlij wiadomość do brokera B
            _LOGGER.debug(f"A->B: {msg.topic} = {msg.payload}")
            self.client_b.publish(msg.topic, msg.payload, qos=msg.qos, retain=msg.retain)
        except Exception as e:
            _LOGGER.error(f"Błąd podczas przekazywania wiadomości A->B: {e}")

    def _on_message_b(self, client, userdata, msg):
        """Callback wywoływany po otrzymaniu wiadomości z brokera B."""
        if not self.running or not self.bidirectional:
            return
            
        try:
            # Prześlij wiadomość do brokera A
            _LOGGER.debug(f"B->A: {msg.topic} = {msg.payload}")
            self.client_a.publish(msg.topic, msg.payload, qos=msg.qos, retain=msg.retain)
        except Exception as e:
            _LOGGER.error(f"Błąd podczas przekazywania wiadomości B->A: {e}")

    def _on_disconnect_a(self, client, userdata, rc):
        """Callback wywoływany po rozłączeniu z brokerem A."""
        if rc != 0:
            _LOGGER.warning(f"Nieoczekiwane rozłączenie z brokerem A, kod: {rc}")

    def _on_disconnect_b(self, client, userdata, rc):
        """Callback wywoływany po rozłączeniu z brokerem B."""
        if rc != 0:
            _LOGGER.warning(f"Nieoczekiwane rozłączenie z brokerem B, kod: {rc}")
