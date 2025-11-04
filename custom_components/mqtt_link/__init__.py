"""MQTT Link Integration - synchronize MQTT messages between two brokers."""
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
    """Set up MQTT Link integration."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up MQTT Link from config entry."""
    mqtt_bridge = MQTTBridge(hass, entry)
    
    hass.data[DOMAIN][entry.entry_id] = mqtt_bridge
    
    # Start bridge
    await hass.async_add_executor_job(mqtt_bridge.start)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload MQTT Link config entry."""
    mqtt_bridge = hass.data[DOMAIN].pop(entry.entry_id)
    await hass.async_add_executor_job(mqtt_bridge.stop)
    return True


class MQTTBridge:
    """Class handling synchronization between two MQTT brokers."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize MQTT Bridge."""
        self.hass = hass
        self.entry = entry
        
        # Get configuration
        config = entry.data
        
        # Configuration for broker A (local Home Assistant)
        self.broker_a_host = config.get("broker_a_host", "localhost")
        self.broker_a_port = config.get("broker_a_port", 1883)
        self.broker_a_username = config.get("broker_a_username")
        self.broker_a_password = config.get("broker_a_password")
        self.broker_a_topic = config.get("broker_a_topic", "#")
        
        # Configuration for broker B (remote Home Assistant)
        self.broker_b_host = config["broker_b_host"]
        self.broker_b_port = config.get("broker_b_port", 1883)
        self.broker_b_username = config.get("broker_b_username")
        self.broker_b_password = config.get("broker_b_password")
        self.broker_b_topic = config.get("broker_b_topic", "#")
        
        # Synchronization options
        self.bidirectional = config.get("bidirectional", True)
        
        # MQTT clients
        self.client_a = None
        self.client_b = None
        
        # Running flag
        self.running = False

    def start(self) -> None:
        """Start MQTT bridge."""
        _LOGGER.info("Starting MQTT Link...")
        
        # Create MQTT clients
        self.client_a = mqtt.Client(client_id="mqtt_link_a")
        self.client_b = mqtt.Client(client_id="mqtt_link_b")
        
        # Set callbacks for client A
        self.client_a.on_connect = self._on_connect_a
        self.client_a.on_message = self._on_message_a
        self.client_a.on_disconnect = self._on_disconnect_a
        
        # Set callbacks for client B
        self.client_b.on_connect = self._on_connect_b
        self.client_b.on_message = self._on_message_b
        self.client_b.on_disconnect = self._on_disconnect_b
        
        # Set authentication for broker A
        if self.broker_a_username:
            self.client_a.username_pw_set(
                self.broker_a_username, 
                self.broker_a_password
            )
        
        # Set authentication for broker B
        if self.broker_b_username:
            self.client_b.username_pw_set(
                self.broker_b_username, 
                self.broker_b_password
            )
        
        try:
            # Connect to broker A
            _LOGGER.info(f"Connecting to broker A: {self.broker_a_host}:{self.broker_a_port}")
            self.client_a.connect(self.broker_a_host, self.broker_a_port, 60)
            
            # Connect to broker B
            _LOGGER.info(f"Connecting to broker B: {self.broker_b_host}:{self.broker_b_port}")
            self.client_b.connect(self.broker_b_host, self.broker_b_port, 60)
            
            # Start network loops
            self.client_a.loop_start()
            self.client_b.loop_start()
            
            self.running = True
            _LOGGER.info("MQTT Link started successfully")
            
        except Exception as e:
            _LOGGER.error(f"Error starting MQTT Link: {e}")
            self.stop()

    def stop(self) -> None:
        """Stop MQTT bridge."""
        _LOGGER.info("Stopping MQTT Link...")
        self.running = False
        
        if self.client_a:
            self.client_a.loop_stop()
            self.client_a.disconnect()
        
        if self.client_b:
            self.client_b.loop_stop()
            self.client_b.disconnect()
        
        _LOGGER.info("MQTT Link stopped")

    def _on_connect_a(self, client, userdata, flags, rc):
        """Callback called after connecting to broker A."""
        if rc == 0:
            _LOGGER.info(f"Connected to broker A, subscribing to: {self.broker_a_topic}")
            client.subscribe(self.broker_a_topic)
        else:
            _LOGGER.error(f"Failed to connect to broker A, code: {rc}")

    def _on_connect_b(self, client, userdata, flags, rc):
        """Callback called after connecting to broker B."""
        if rc == 0:
            _LOGGER.info(f"Connected to broker B, subscribing to: {self.broker_b_topic}")
            if self.bidirectional:
                client.subscribe(self.broker_b_topic)
        else:
            _LOGGER.error(f"Failed to connect to broker B, code: {rc}")

    def _on_message_a(self, client, userdata, msg):
        """Callback called after receiving message from broker A."""
        if not self.running:
            return
            
        try:
            # Forward message to broker B
            _LOGGER.debug(f"A->B: {msg.topic} = {msg.payload}")
            self.client_b.publish(msg.topic, msg.payload, qos=msg.qos, retain=msg.retain)
        except Exception as e:
            _LOGGER.error(f"Error forwarding message A->B: {e}")

    def _on_message_b(self, client, userdata, msg):
        """Callback called after receiving message from broker B."""
        if not self.running or not self.bidirectional:
            return
            
        try:
            # Forward message to broker A
            _LOGGER.debug(f"B->A: {msg.topic} = {msg.payload}")
            self.client_a.publish(msg.topic, msg.payload, qos=msg.qos, retain=msg.retain)
        except Exception as e:
            _LOGGER.error(f"Error forwarding message B->A: {e}")

    def _on_disconnect_a(self, client, userdata, rc):
        """Callback called after disconnecting from broker A."""
        if rc != 0:
            _LOGGER.warning(f"Unexpected disconnection from broker A, code: {rc}")

    def _on_disconnect_b(self, client, userdata, rc):
        """Callback called after disconnecting from broker B."""
        if rc != 0:
            _LOGGER.warning(f"Unexpected disconnection from broker B, code: {rc}")
