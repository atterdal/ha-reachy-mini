# Changelog

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
