#!/usr/bin/with-contenv bashio
# ==============================================================================
# Startar Reachy Mini Lite-daemonen + förbereder ljud, HA-verktyg och röst.
# ==============================================================================
set -e

# Persistent lagring för HuggingFace-modeller/cache + ~/.asoundrc.
export HOME="/data"
export HF_HOME="/data/hf"
export XDG_CACHE_HOME="/data/cache"
mkdir -p "${HF_HOME}" "${XDG_CACHE_HOME}"

# --- ALSA: peka ut Reachys USB-ljudkort ---------------------------------------
# I en container hittar daemonen inte ljudkorten "by name" (/proc/asound saknas),
# så ALSA "default" pekar på fel kort (HDMI) → tyst röst. Daemonen använder dock
# namngivna enheter reachymini_audio_src/_sink (dsnoop/dmix) om ~/.asoundrc finns.
# Vi genererar den med daemonens egen funktion (autodetekterar kortnr via arecord).
bashio::log.info "Genererar ALSA-config för Reachy-ljudkortet (~/.asoundrc)..."
if /opt/reachy/bin/python -c "from reachy_mini.media.audio_utils import write_asoundrc_to_home; write_asoundrc_to_home()"; then
  bashio::log.info "ALSA-config skriven."
else
  bashio::log.warning "Kunde inte skriva ~/.asoundrc — ljud (mic/högtalare) kan saknas."
fi

# --- HA-verktyg för conversation-appen ----------------------------------------
# home_assistant-verktyget laddas automatiskt av conversation-appen och låter
# roboten styra Home Assistant via Assist (http://supervisor/core/api).
export REACHY_MINI_EXTERNAL_TOOLS_DIRECTORY="/opt/reachy-ha-tools"
export AUTOLOAD_EXTERNAL_TOOLS="true"

# --- Röst-backend: OpenAI Realtime om nyckel angetts, annars gratis HF-röst ----
if bashio::config.has_value 'openai_api_key'; then
  export OPENAI_API_KEY="$(bashio::config 'openai_api_key')"
  export BACKEND_PROVIDER="openai"
  if bashio::config.has_value 'model_name'; then
    export MODEL_NAME="$(bashio::config 'model_name')"
  fi
  bashio::log.info "Röst-backend: OpenAI Realtime (modell: ${MODEL_NAME:-gpt-realtime-2})"
else
  bashio::log.info "Ingen OpenAI-nyckel satt — conversation-appen använder gratis HF-röst."
fi

bashio::log.info "Letar efter Reachy Mini på USB..."
if [ -d /dev/serial/by-id ]; then
  bashio::log.info "Serieportar: $(ls /dev/serial/by-id 2>/dev/null | tr '\n' ' ')"
fi

bashio::log.info "Startar reachy-mini-daemon (Lite) — dashboard/API på port 8000"
exec reachy-mini-daemon
