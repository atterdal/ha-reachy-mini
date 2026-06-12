# Changelog

## 0.1.1

- Bygg-fix: lägg till Cairo/GObject-introspection-dev-headers + meson/ninja så
  pycairo/PyGObject kan kompileras (bygget föll på `pycairo metadata-generation-failed`).

## 0.1.0

- Första versionen.
- Kör `reachy-mini-daemon` (Reachy Mini Lite) som ett HAOS add-on på amd64.
- `full_access` + `udev` + `host_network` för USB-hårdvara och port 8000.
- GStreamer-mediastack + `reachy-mini` (PyPI) installeras i bygget.
