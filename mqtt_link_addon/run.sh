#!/usr/bin/with-contenv bashio
# ==============================================================================
# MQTT Unified Broker Add-on for Home Assistant
# ==============================================================================

bashio::log.info "Starting MQTT Unified Broker..."

# Display configuration summary
bashio::log.info "Configuration:"
bashio::log.info "- Listen: $(bashio::config 'listen.host'):$(bashio::config 'listen.port')"
bashio::log.info "- Discovery prefix: $(bashio::config 'discovery_prefix')"
bashio::log.info "- LRU cache: $(bashio::config 'max_lru') entries, TTL: $(bashio::config 'retain_cache_ttl_sec')s"
bashio::log.info "- Log level: $(bashio::config 'log_level')"

# Count upstreams
UPSTREAM_COUNT=$(bashio::config 'upstreams | length')
bashio::log.info "- Upstreams: ${UPSTREAM_COUNT}"

for i in $(seq 0 $((UPSTREAM_COUNT - 1))); do
    UP_ID=$(bashio::config "upstreams[${i}].id")
    UP_HOST=$(bashio::config "upstreams[${i}].host")
    UP_PORT=$(bashio::config "upstreams[${i}].port")
    bashio::log.info "  * ${UP_ID}: ${UP_HOST}:${UP_PORT}"
done

# Run the unified broker
cd /app
exec node dist/index.js
