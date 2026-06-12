# Reachy Mini (HAOS add-on)

Kör Pollen/HuggingFace **Reachy Mini Lite**-daemonen direkt på din Home
Assistant-maskin (NUC). Daemonen pratar med roboten över USB och serverar ett
REST/WebSocket-API + dashboard på **port 8000**.

## Förkrav

- **HAOS på x86_64** (NUC). Add-onen byggs bara för `amd64`.
- Reachy Mini **Lite** ansluten med USB-C till samma maskin, och robotens
  nätadapter inkopplad i vägguttaget.

## Installation

> Add-onen kör en **förbyggd image** från GHCR — Supervisor gör bara en
> `docker pull`, inget kompileras på NUC:en.

1. **Engångssteg (repo-ägaren):** efter att GitHub Actions-bygget
   (`Build add-on image`) gått klart, gör GHCR-paketet **publikt** så Supervisor
   kan hämta det utan inloggning: GitHub → din profil → **Packages** →
   `amd64-reachy-mini` → **Package settings** → **Change visibility → Public**.
2. **Settings → Add-ons → Add-on Store → ⋮ (uppe till höger) → Repositories**
   och lägg till: `https://github.com/atterdal/ha-reachy-mini`
3. Öppna **Reachy Mini** → **Install** (snabb — bara en pull).
4. Koppla in roboten via USB, slå på den, och klicka **Start**.
5. Öppna fliken **Log** och vänta tills daemonen hittat roboten.

## Använda roboten

Daemonen lyssnar på `http://<NUC-IP>:8000`. Eftersom add-onen kör med
`host_network` är porten direkt nåbar på maskinens IP.

- **Dashboard:** `http://<NUC-IP>:8000`
- **Python SDK** (från valfri dator på nätet):
  ```python
  from reachy_mini import ReachyMini
  reachy = ReachyMini(host="<NUC-IP>")  # ansluter till daemonen
  ```
- **3D-card i Lovelace:** installera HACS-cardet
  [`Desmond-Dong/ha-reachy-mini`](https://github.com/Desmond-Dong/ha-reachy-mini)
  och peka det på `host: <NUC-IP>`, `port: 8000`.

## Hårdvaruåtkomst

Add-onen kör med `full_access` + `udev` så att containern ser **all** USB-hårdvara
— den seriella motorstyrningen (WCH-chip `1a86:55d3`), USB-ljudenheten
(`38fb:1001`, mikrofoner + högtalare) och en ev. kamera (`/dev/video*`). Det är
brett men rimligt på en dedikerad robotlåda. Vill man strama åt senare kan man
byta `full_access` mot explicita `devices:`/`uart:`/`usb:`-rader.

## Felsökning

- **Hittar inte roboten:** kolla `Log`-fliken. Verifiera i en SSH/Terminal-addon
  att `ls /dev/serial/by-id` visar en enhet när roboten är inkopplad. WCH-serie­chip
  kan dyka upp som `/dev/ttyACM0` eller `/dev/ttyUSB0`.
- **Inget ljud / mikrofon:** kontrollera att USB-ljudenheten finns med i
  `ashell`/`arecord -l`. Reachy använder GStreamer/ALSA, inte HA:s PulseAudio.
- **Bygget misslyckas på ett GStreamer-paket:** öppna en issue så justerar vi
  paketlistan i `Dockerfile` — beroenden i `reachy-mini` ändras ibland.

## Status

v0.1.0 — första versionen, bara daemonen (robot "levande" och styrbar).
Röst/Assist-integration är ett planerat nästa steg.
