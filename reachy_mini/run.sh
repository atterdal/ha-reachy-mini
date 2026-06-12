#!/usr/bin/with-contenv bashio
# ==============================================================================
# Startar Reachy Mini Lite-daemonen.
# Daemonen autodetekterar roboten via USB (seriell motorstyrning + USB-ljud)
# och serverar REST/WebSocket + dashboard på port 8000 (host_network).
# ==============================================================================
set -e

# Persistent lagring för HuggingFace-modeller/cache så de inte laddas ned varje
# omstart. /data är add-onens beständiga volym.
export HOME="/data"
export HF_HOME="/data/hf"
export XDG_CACHE_HOME="/data/cache"
mkdir -p "${HF_HOME}" "${XDG_CACHE_HOME}"

bashio::log.info "Letar efter Reachy Mini på USB..."
if [ -d /dev/serial/by-id ]; then
  bashio::log.info "Serieportar: $(ls /dev/serial/by-id 2>/dev/null | tr '\n' ' ')"
fi

bashio::log.info "Startar reachy-mini-daemon (Lite) — dashboard/API på port 8000"
exec reachy-mini-daemon
