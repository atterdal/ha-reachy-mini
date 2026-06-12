# Changelog

## 0.4.0

- **Ljud-fix permanent:** run.sh genererar `~/.asoundrc` (reachymini_audio_src/_sink,
  dmix/dsnoop) vid start så daemonen hittar Reachys USB-mic/högtalare i containern.
- **HA-styrning:** bakar in `home_assistant`-verktyget (`/opt/reachy-ha-tools/`) +
  `REACHY_MINI_EXTERNAL_TOOLS_DIRECTORY`/`AUTOLOAD_EXTERNAL_TOOLS`, och
  `homeassistant_api: true` så roboten kan styra hemmet via HA:s Assist.
- **OpenAI Realtime-röst:** ny add-on-inställning `openai_api_key` (+ `model_name`).
  Satt → `BACKEND_PROVIDER=openai`; tom → gratis HF-röst.

## 0.3.0

- **Mediastack: bakar in GStreamers rust-webrtc-plugin (`webrtcsink`).** Utan det
  startar daemonens `GstMediaServer` inte → varken lokal IPC eller webrtc kommer
  upp → conversation-appen kraschar (`ConnectionRefused` mot webrtc-signalling) och
  ingen kamera/ljud. Plugin:et finns inte i apt; multi-stage-bygget kompilerar
  `gst-plugin-webrtc` 0.14.5 (cargo-c) mot GStreamer 1.22 och kopierar in det.
  Lägger även till `gstreamer1.0-nice`/`libnice10`/`gstreamer1.0-alsa`.

## 0.2.1

- `apparmor: false` + `privileged: [SYS_NICE, SYS_RAWIO]`. HA:s sandlåda
  (AppArmor + begränsade capabilities) blockerade serie-/motoroperationerna
  (`Failed to start daemon: Operation not permitted`) trots `full_access`.

## 0.2.0

- **Förbyggd image.** Imagen byggs nu i GitHub Actions och publiceras till GHCR
  (`ghcr.io/atterdal/amd64-reachy-mini`). `config.yaml` pekar på `image:`, så
  Supervisor bara hämtar (docker pull) i stället för att kompilera på NUC:en.
  Löser kraschen/jobblåset som tunga lokala bygget (pycairo/PyGObject) orsakade.

## 0.1.1

- Bygg-fix: lägg till Cairo/GObject-introspection-dev-headers + meson/ninja så
  pycairo/PyGObject kan kompileras (bygget föll på `pycairo metadata-generation-failed`).

## 0.1.0

- Första versionen.
- Kör `reachy-mini-daemon` (Reachy Mini Lite) som ett HAOS add-on på amd64.
- `full_access` + `udev` + `host_network` för USB-hårdvara och port 8000.
- GStreamer-mediastack + `reachy-mini` (PyPI) installeras i bygget.
