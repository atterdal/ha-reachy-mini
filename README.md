# Reachy Mini – Home Assistant add-on

Ett HAOS add-on-repo som kör **Reachy Mini Lite**-daemonen direkt på din Home
Assistant-maskin, så roboten styrs över USB utan en separat dator.

## Snabbstart

1. Settings → Add-ons → Add-on Store → **⋮ → Repositories**
2. Lägg till: `https://github.com/atterdal/ha-reachy-mini`
3. Installera **Reachy Mini**, koppla in roboten via USB och starta add-onen.

Full dokumentation finns i [`reachy_mini/DOCS.md`](reachy_mini/DOCS.md).

## Innehåll

- [`reachy_mini/`](reachy_mini/) – själva add-onen
  - `config.yaml` – add-on-metadata + hårdvaruåtkomst
  - `Dockerfile` / `build.yaml` – bygger en amd64-image med GStreamer + `reachy-mini`
  - `run.sh` – startar `reachy-mini-daemon`
  - `DOCS.md` – användarguide (visas i add-onens Documentation-flik)

## Förkrav

- HAOS på **x86_64** (t.ex. en Intel NUC)
- Reachy Mini **Lite** ansluten via USB-C

## Licens

MIT
