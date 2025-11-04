#!/usr/bin/env python3
"""MQTT Mirror Link - Bridge between two MQTT brokers."""
import argparse
import logging
import signal
import sys
import time
import hashlib
from collections import OrderedDict
import paho.mqtt.client as mqtt

_LOGGER = logging.getLogger(__name__)


class MQTTBridge:
    """MQTT Bridge class."""

    def __init__(self, args):
        """Initialize the bridge."""
        self.args = args
        self.running = False
        
        # Loop prevention: Track recently forwarded messages
        self.message_cache = OrderedDict()
        self.max_cache_size = 1000
        
        # Klienci MQTT
        self.client_a = mqtt.Client(client_id="mqtt_bridge_a")
        self.client_b = mqtt.Client(client_id="mqtt_bridge_b")
        
        # Callbacks
        self.client_a.on_connect = self._on_connect_a
        self.client_a.on_message = self._on_message_a
        self.client_a.on_disconnect = self._on_disconnect_a
        
        self.client_b.on_connect = self._on_connect_b
        self.client_b.on_message = self._on_message_b
        self.client_b.on_disconnect = self._on_disconnect_b
        
        # Uwierzytelnianie
        if args.broker_a_username:
            self.client_a.username_pw_set(
                args.broker_a_username,
                args.broker_a_password
            )
        
        if args.broker_b_username:
            self.client_b.username_pw_set(
                args.broker_b_username,
                args.broker_b_password
            )

    def _on_connect_a(self, client, userdata, flags, rc):
        """Callback for broker A connection."""
        if rc == 0:
            _LOGGER.info(f"Connected to broker A, subscribing to: {self.args.broker_a_topic}")
            client.subscribe(self.args.broker_a_topic)
        else:
            _LOGGER.error(f"Failed to connect to broker A, code: {rc}")

    def _on_connect_b(self, client, userdata, flags, rc):
        """Callback for broker B connection."""
        if rc == 0:
            _LOGGER.info(f"Connected to broker B, subscribing to: {self.args.broker_b_topic}")
            if self.args.bidirectional:
                client.subscribe(self.args.broker_b_topic)
        else:
            _LOGGER.error(f"Failed to connect to broker B, code: {rc}")

    def _is_duplicate(self, topic, payload, direction):
        """Check if message is a duplicate (loop prevention)."""
        if not self.args.loop_prevention:
            return False
            
        # Create message fingerprint
        msg_hash = hashlib.md5(f"{topic}:{payload}:{direction}".encode()).hexdigest()
        current_time = time.time()
        
        # Check if message was recently forwarded
        if msg_hash in self.message_cache:
            last_time = self.message_cache[msg_hash]
            if current_time - last_time < self.args.message_ttl:
                _LOGGER.debug(f"Duplicate detected: {topic} (direction: {direction})")
                return True
        
        # Add to cache
        self.message_cache[msg_hash] = current_time
        
        # Limit cache size
        if len(self.message_cache) > self.max_cache_size:
            self.message_cache.popitem(last=False)
            
        return False

    def _on_message_a(self, client, userdata, msg):
        """Callback for messages from broker A."""
        if not self.running:
            return
            
        # Check for duplicates
        if self._is_duplicate(msg.topic, msg.payload, "A->B"):
            return
            
        try:
            _LOGGER.debug(f"A->B: {msg.topic} = {msg.payload}")
            self.client_b.publish(msg.topic, msg.payload, qos=msg.qos, retain=msg.retain)
        except Exception as e:
            _LOGGER.error(f"Error forwarding message A->B: {e}")

    def _on_message_b(self, client, userdata, msg):
        """Callback for messages from broker B."""
        if not self.running or not self.args.bidirectional:
            return
            
        # Check for duplicates
        if self._is_duplicate(msg.topic, msg.payload, "B->A"):
            return
            
        try:
            _LOGGER.debug(f"B->A: {msg.topic} = {msg.payload}")
            self.client_a.publish(msg.topic, msg.payload, qos=msg.qos, retain=msg.retain)
        except Exception as e:
            _LOGGER.error(f"Error forwarding message B->A: {e}")

    def _on_disconnect_a(self, client, userdata, rc):
        """Callback for broker A disconnection."""
        if rc != 0:
            _LOGGER.warning(f"Unexpected disconnection from broker A, code: {rc}")

    def _on_disconnect_b(self, client, userdata, rc):
        """Callback for broker B disconnection."""
        if rc != 0:
            _LOGGER.warning(f"Unexpected disconnection from broker B, code: {rc}")

    def start(self):
        """Start the bridge."""
        _LOGGER.info("Starting MQTT Mirror Link...")
        
        try:
            # Połącz z brokerami
            _LOGGER.info(f"Connecting to broker A: {self.args.broker_a_host}:{self.args.broker_a_port}")
            self.client_a.connect(self.args.broker_a_host, self.args.broker_a_port, 60)
            
            _LOGGER.info(f"Connecting to broker B: {self.args.broker_b_host}:{self.args.broker_b_port}")
            self.client_b.connect(self.args.broker_b_host, self.args.broker_b_port, 60)
            
            # Uruchom pętle
            self.client_a.loop_start()
            self.client_b.loop_start()
            
            self.running = True
            _LOGGER.info("MQTT Mirror Link started successfully")
            
            # Czekaj
            while self.running:
                time.sleep(1)
                
        except Exception as e:
            _LOGGER.error(f"Error starting MQTT Mirror Link: {e}")
            self.stop()
    # Options
    parser.add_argument("--bidirectional", type=lambda x: x.lower() == 'true', default=True, help="Bidirectional sync")
    parser.add_argument("--log-level", default="info", choices=["debug", "info", "warning", "error"], help="Log level")
    parser.add_argument("--loop-prevention", type=lambda x: x.lower() == 'true', default=True, help="Enable loop prevention")
    parser.add_argument("--message-ttl", type=int, default=2, help="Message TTL in seconds for loop prevention")
    
    return parser.parse_args()
        
        if self.client_a:
            self.client_a.loop_stop()
            self.client_a.disconnect()
        
        if self.client_b:
            self.client_b.loop_stop()
            self.client_b.disconnect()
        
        _LOGGER.info("MQTT Mirror Link stopped")


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="MQTT Mirror Link")
    
    # Broker A
    parser.add_argument("--broker-a-host", required=True, help="Broker A host")
    parser.add_argument("--broker-a-port", type=int, default=1883, help="Broker A port")
    parser.add_argument("--broker-a-username", default="", help="Broker A username")
    parser.add_argument("--broker-a-password", default="", help="Broker A password")
    parser.add_argument("--broker-a-topic", default="#", help="Broker A topic")
    
    # Broker B
    parser.add_argument("--broker-b-host", required=True, help="Broker B host")
    parser.add_argument("--broker-b-port", type=int, default=1883, help="Broker B port")
    parser.add_argument("--broker-b-username", default="", help="Broker B username")
    parser.add_argument("--broker-b-password", default="", help="Broker B password")
    parser.add_argument("--broker-b-topic", default="#", help="Broker B topic")
    
    # Options
    parser.add_argument("--bidirectional", type=lambda x: x.lower() == 'true', default=True, help="Bidirectional sync")
    parser.add_argument("--log-level", default="info", choices=["debug", "info", "warning", "error"], help="Log level")
    
    return parser.parse_args()


def setup_logging(level):
    """Setup logging."""
    numeric_level = getattr(logging, level.upper(), None)
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def main():
    """Main function."""
    args = parse_args()
    setup_logging(args.log_level)
    
    bridge = MQTTBridge(args)
    
    # Handle signals
    def signal_handler(signum, frame):
        _LOGGER.info("Received signal, stopping...")
        bridge.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start bridge
    bridge.start()


if __name__ == "__main__":
    main()
