FROM ubuntu:24.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    coreutils \
    findutils \
    grep \
    sed \
    gawk \
    procps \
    tree \
    man-db \
    less \
    file \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /exercise
