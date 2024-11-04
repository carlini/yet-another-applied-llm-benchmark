# Use an official Ubuntu as a parent image
FROM ubuntu:latest

# Update the system and install dependencies
RUN apt-get update && apt-get install -y \
    software-properties-common

# Add the deadsnakes PPA, which contains newer Python versions
RUN add-apt-repository ppa:deadsnakes/ppa


# Update the system and install Python and build dependencies
RUN apt-get update && apt-get install -y \
    software-properties-common \
    build-essential \
    gcc \
    curl \
    sqlite3 \
    gdb \
    libssl-dev

ENV DEBIAN_FRONTEND noninteractive

# Install Python 3.11
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-venv \
    python3.11-dev \
    python3-pip \
    git

RUN ln -s /usr/bin/python3.11 /usr/bin/python
RUN rm /usr/bin/pip
RUN ln -s /usr/bin/pip3.11 /usr/bin/pip
RUN rm /usr/bin/python3
RUN rm /usr/bin/pip3
RUN ln -s /usr/bin/python3.11 /usr/bin/python3
RUN ln -s /usr/bin/pip3.11 /usr/bin/pip3

RUN echo '#!/bin/bash\n"$@"' > /usr/bin/sudo && \
    chmod +x /usr/bin/sudo

RUN python3.11 -m pip install --upgrade pip && \
    pip install numpy scipy numba Pillow jax jaxlib python-chess torch


# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Ensure Rust binaries are in PATH
ENV PATH="/root/.cargo/bin:${PATH}"

# Set the working directory in the container
WORKDIR /usr/src/app

# Any additional commands or environment variables can be added here

# Command to run when the container launches
CMD ["/bin/bash"]
