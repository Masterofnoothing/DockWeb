FROM debian:stable-slim

# Set environment variables
ENV GIT_USERNAME=sryze
ENV GIT_REPO=crx-dl
ENV ISDOCKER=true

# Install necessary packages
RUN apt update && \
    apt upgrade -y && \
    apt install -y --no-install-recommends \
        curl \
        wget \
        git \
        chromium \
        chromium-driver \
        python3 \
        python3-pip \
        python3-flask \
        python3-requests \
        python3-selenium && \
    apt autoremove --purge -y && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Download crx downloader from GitHub
RUN git clone "https://github.com/${GIT_USERNAME}/${GIT_REPO}.git" && \
    chmod +x ./${GIT_REPO}/crx-dl.py

# Copy project files
COPY . .

# Set entrypoint
ENTRYPOINT ["python3", "main.py"]

EXPOSE 5000