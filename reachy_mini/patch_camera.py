"""Patch reachy_mini.find_video_device for GStreamer v4l2 device-path key.

Some GStreamer versions expose the v4l2 device path as the property
``device.path`` (with ``device.api == "v4l2"``) instead of ``api.v4l2.path``.
``find_video_device`` only checks ``api.v4l2.path``, so the camera is detected
but then discarded → "No camera found". Accept both keys.

Run with the venv python at build time:  /opt/reachy/bin/python patch_camera.py
"""

import sys
import reachy_mini.media.device_detection as m

f = m.__file__
s = open(f).read()
orig = s

s = s.replace(
    'if "api.v4l2.path" in props:',
    'if "api.v4l2.path" in props or "device.path" in props:',
)
s = s.replace(
    'device_path = props["api.v4l2.path"]',
    'device_path = props.get("api.v4l2.path") or props["device.path"]',
)

if s == orig:
    print(f"patch_camera: strings not found in {f} — already patched or upstream changed", file=sys.stderr)
    # Don't fail the build: newer GStreamer may already use api.v4l2.path.
    sys.exit(0)

open(f, "w").write(s)
print(f"patch_camera: applied to {f}")
