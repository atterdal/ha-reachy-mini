ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base-debian:bookworm
FROM ${BUILD_FROM}

ENV LANG=C.UTF-8 \
    PYTHONUNBUFFERED=1

# System-beroenden: Python, git(+LFS för modellfiler), GStreamer-mediastacken
# som Reachy använder för kamera/ljud, samt ALSA/PortAudio för USB-mikrofon
# och högtalare. python3-gi/python3-gst behövs för Pythons GStreamer-bindningar.
RUN apt-get update && apt-get install -y --no-install-recommends \
      python3 python3-venv python3-pip python3-dev \
      python3-gi python3-gst-1.0 gir1.2-gstreamer-1.0 gir1.2-gst-plugins-base-1.0 \
      build-essential pkg-config meson ninja-build \
      libcairo2-dev libgirepository1.0-dev gobject-introspection \
      git git-lfs curl ca-certificates \
      libgstreamer1.0-0 libgstreamer-plugins-base1.0-0 \
      gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
      gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
      gstreamer1.0-libav gstreamer1.0-tools \
      libportaudio2 libasound2 alsa-utils \
      ffmpeg \
    && git lfs install \
    && rm -rf /var/lib/apt/lists/*

# Reachy installeras i en venv med tillgång till systemets gi/gst-bindningar.
# (Debian bookworm blockerar pip mot system-Python; venv löser det.)
RUN python3 -m venv --system-site-packages /opt/reachy \
    && /opt/reachy/bin/pip install --no-cache-dir --upgrade pip \
    && /opt/reachy/bin/pip install --no-cache-dir "reachy-mini"

ENV PATH="/opt/reachy/bin:${PATH}"

COPY run.sh /run.sh
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
