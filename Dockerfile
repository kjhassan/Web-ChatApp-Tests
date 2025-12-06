FROM python:3.11-slim

RUN apt-get update && apt-get install -y wget gnupg unzip \
    libnss3 libgconf-2-4 libxi6 libappindicator3-1 libgbm1 libxrandr2 libxss1 libasound2 \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get update && apt-get install -y /tmp/chrome.deb \
    && rm /tmp/chrome.deb

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["pytest", "-q", "--junitxml=report.xml"]
