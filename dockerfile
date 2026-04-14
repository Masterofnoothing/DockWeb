FROM debian:stable-slim

# Set environment variables
ENV ISDOCKER=true

# Install necessary packages
RUN apt update && \
    apt upgrade -y && \
    apt install -y --no-install-recommends \
        curl \
        wget \
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

# Copy project files
COPY . .

# Set entrypoint
ENTRYPOINT ["python3", "main.py"]

EXPOSE 5000
