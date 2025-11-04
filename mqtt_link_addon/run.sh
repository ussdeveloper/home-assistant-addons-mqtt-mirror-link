#!/usr/bin/with-contenv bashio
# ==============================================================================
# MQTT Mirror Link Add-on for Home Assistant
# ==============================================================================

bashio::log.info "Starting MQTT Mirror Link..."

# Get configuration
BROKER_A_HOST=$(bashio::config 'broker_a.host')
BROKER_A_PORT=$(bashio::config 'broker_a.port')
BROKER_A_USERNAME=$(bashio::config 'broker_a.username')
BROKER_A_PASSWORD=$(bashio::config 'broker_a.password')
BROKER_A_TOPIC=$(bashio::config 'broker_a.topic')

BROKER_B_HOST=$(bashio::config 'broker_b.host')
BROKER_B_PORT=$(bashio::config 'broker_b.port')
BROKER_B_USERNAME=$(bashio::config 'broker_b.username')
BROKER_B_PASSWORD=$(bashio::config 'broker_b.password')
BROKER_B_TOPIC=$(bashio::config 'broker_b.topic')

BIDIRECTIONAL=$(bashio::config 'bidirectional')
LOG_LEVEL=$(bashio::config 'log_level')

bashio::log.info "Broker A: ${BROKER_A_HOST}:${BROKER_A_PORT}"
bashio::log.info "Broker B: ${BROKER_B_HOST}:${BROKER_B_PORT}"
bashio::log.info "Bidirectional: ${BIDIRECTIONAL}"

# Start Python application
exec python3 /app/mqtt_bridge.py \
    --broker-a-host "${BROKER_A_HOST}" \
    --broker-a-port "${BROKER_A_PORT}" \
    --broker-a-username "${BROKER_A_USERNAME}" \
    --broker-a-password "${BROKER_A_PASSWORD}" \
    --broker-a-topic "${BROKER_A_TOPIC}" \
    --broker-b-host "${BROKER_B_HOST}" \
    --broker-b-port "${BROKER_B_PORT}" \
    --broker-b-username "${BROKER_B_USERNAME}" \
    --broker-b-password "${BROKER_B_PASSWORD}" \
    --broker-b-topic "${BROKER_B_TOPIC}" \
    --bidirectional "${BIDIRECTIONAL}" \
    --log-level "${LOG_LEVEL}"
