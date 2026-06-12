ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base-debian:bookworm

# ============================================================================
# Steg 1: kompilera GStreamers rust-webrtc-plugin (webrtcsink).
# Det finns inte som apt-paket — Pollen kräver bygge från källa, pinnat till
# 0.14.5 (kritisk webrtcsink-deadlock-fix). Byggs mot SAMMA GStreamer (1.22)
# som runtime-steget så ABI:t matchar. Allt tungt sker i CI, inte på NUC:en.
# ============================================================================
FROM ${BUILD_FROM} AS webrtc-builder

RUN apt-get update && apt-get install -y --no-install-recommends \
      curl ca-certificates git build-essential pkg-config \
      libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev \
      libgstreamer-plugins-bad1.0-dev \
      libglib2.0-dev libssl-dev libnice-dev \
    && rm -rf /var/lib/apt/lists/*

# Rust + cargo-c
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal
ENV PATH="/root/.cargo/bin:${PATH}"
RUN cargo install cargo-c --locked

# Bygg och installera webrtc-plugin:et till /opt/gst-plugins-rs
RUN git clone --depth 1 --branch 0.14.5 \
      https://gitlab.freedesktop.org/gstreamer/gst-plugins-rs.git /src \
    && cd /src \
    && cargo cinstall -p gst-plugin-webrtc \
         --prefix=/opt/gst-plugins-rs --libdir=/opt/gst-plugins-rs/lib --release

# ============================================================================
# Steg 2: runtime-imagen (daemon + reachy-mini + mediastack + webrtc-plugin)
# ============================================================================
FROM ${BUILD_FROM}

ENV LANG=C.UTF-8 \
    PYTHONUNBUFFERED=1

# System-beroenden: Python, git(+LFS), GStreamer-mediastacken (kamera/ljud),
# ALSA/PortAudio för USB-mikrofon/högtalare, libnice/gstreamer-nice för webrtc-ICE.
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
      gstreamer1.0-nice gstreamer1.0-alsa libnice10 \
      libportaudio2 libasound2 alsa-utils \
      ffmpeg \
    && git lfs install \
    && rm -rf /var/lib/apt/lists/*

# Reachy installeras i en venv med tillgång till systemets gi/gst-bindningar.
RUN python3 -m venv --system-site-packages /opt/reachy \
    && /opt/reachy/bin/pip install --no-cache-dir --upgrade pip \
    && /opt/reachy/bin/pip install --no-cache-dir "reachy-mini"

# Bakade-in webrtc-plugin:et från byggsteget + säg åt GStreamer var det ligger.
COPY --from=webrtc-builder /opt/gst-plugins-rs /opt/gst-plugins-rs
ENV GST_PLUGIN_PATH=/opt/gst-plugins-rs/lib/gstreamer-1.0

ENV PATH="/opt/reachy/bin:${PATH}"

COPY run.sh /run.sh
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
