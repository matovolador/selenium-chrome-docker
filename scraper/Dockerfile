# Use the official Python base image
FROM python:3.10.4

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Update and install minimal dependencies
RUN apt-get update \
    && apt-get install -y \
        wget \
        gnupg \
        curl \
        fonts-liberation \
        libu2f-udev \
        xdg-utils \
        libnss3 \
        cron \
        libgbm1 \
        libatk-bridge2.0-0 \
        libgtk-3-0 \
        libx11-xcb1 \
        # Clean up package lists to reduce image size
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

# Add Google's official GPG key and repository
RUN curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update

# Install Google Chrome
RUN apt-get install -y google-chrome-stable

# Set work directory
RUN mkdir /app
WORKDIR /app

# Copy files
COPY . /app/

# Install pip requirements
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Set PYTHONPATH environment variable
ENV PYTHONPATH=/app

# Copy cron jobs and setup cron
COPY cron-jobs /etc/cron.d/cron-jobs
RUN chmod 0644 /etc/cron.d/cron-jobs \
    && crontab /etc/cron.d/cron-jobs \
    && touch /var/log/cron.log

# Command to start cron and tail the log file
CMD cron && tail -f /var/log/cron.log