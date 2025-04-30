# Multi-stage build
FROM nvidia/cuda:12.0.0-cudnn8-runtime-ubuntu22.04 as builder

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHON_VERSION=3.12.0 \
    LDFLAGS="-Wl,--strip-all" \
    CFLAGS="-g0 -O3"

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    wget \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libffi-dev \
    liblzma-dev \
    libsqlite3-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libreadline-dev \
    tk-dev \
    && rm -rf /var/lib/apt/lists/*

# Download and install Python
RUN wget --no-verbose https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz && \
    tar -xJf Python-${PYTHON_VERSION}.tar.xz && \
    cd Python-${PYTHON_VERSION} && \
    ./configure \
        --enable-optimizations \
        --with-lto \
        --enable-shared \
        --without-ensurepip \
        --with-system-ffi \
        --with-system-expat \
        --disable-test-modules \
        --enable-ipv6 \
        --with-computed-gotos && \
    make -j$(($(nproc)-1)) && \
    make altinstall && \
    ldconfig && \
    cd .. && \
    rm -rf Python-${PYTHON_VERSION} Python-${PYTHON_VERSION}.tar.xz

# Install pip
RUN wget --no-verbose https://bootstrap.pypa.io/get-pip.py && \
    /usr/local/bin/python3.12 get-pip.py && \
    rm get-pip.py

# Final stage
FROM nvidia/cuda:12.0.0-cudnn8-runtime-ubuntu22.04

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libssl3 \
    zlib1g \
    libexpat1 \
    libgomp1 \
    libsqlite3-0 \
    libreadline8 \
    libtinfo6 \
    && rm -rf /var/lib/apt/lists/*

# Copy Python installation
COPY --from=builder /usr/local/ /usr/local/
RUN ldconfig

# Create symlink for python command
RUN ln -s /usr/local/bin/python3.12 /usr/local/bin/python && \
    ln -s /usr/local/bin/python3.12 /usr/local/bin/python3

# Setup application
WORKDIR /app
COPY . .

# Fix line endings if needed
RUN if [ -f entrypoint.sh ]; then \
    apt-get update && \
    apt-get install -y --no-install-recommends dos2unix && \
    chmod +x entrypoint.sh && \
    dos2unix entrypoint.sh && \
    apt-get purge -y --auto-remove dos2unix && \
    rm -rf /var/lib/apt/lists/*; \
    fi

# Install Python dependencies
RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["/app/entrypoint.sh"]