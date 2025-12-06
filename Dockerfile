FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl \
    libnss3 libxi6 libappindicator3-1 libgbm1 \
    libxrandr2 libxss1 libasound2 libxshmfence1 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get update && apt-get install -y /tmp/chrome.deb \
    && rm /tmp/chrome.deb

# Install Chromedriver (matches installed Chrome version)
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}') && \
    CHROMEDRIVER_VERSION=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json" \
        | python3 -c "import sys,json; data=json.load(sys.stdin); print(data['channels']['Stable']['version'])") && \
    wget -q -O /tmp/chromedriver.zip \
        "https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /tmp/ && \
    mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /tmp/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# IMPORTANT: write JUnit report where Jenkins can see it
CMD ["pytest", "-vv", "--junitxml=/workspace/report.xml"]






# FROM python:3.11-slim

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     wget gnupg unzip curl \
#     libnss3 libgconf-2-4 libxi6 libappindicator3-1 libgbm1 \
#     libxrandr2 libxss1 libasound2 libxshmfence1 \
#     && rm -rf /var/lib/apt/lists/*

# # Install Google Chrome
# RUN wget -q -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
#     && apt-get update && apt-get install -y /tmp/chrome.deb \
#     && rm /tmp/chrome.deb

# # Install Chromedriver (matches installed Chrome version)
# RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}') && \
#     CHROMEDRIVER_VERSION=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json" \
#         | python3 -c "import sys,json; data=json.load(sys.stdin); print(data['channels']['Stable']['version'])") && \
#     wget -q -O /tmp/chromedriver.zip \
#         "https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip" && \
#     unzip /tmp/chromedriver.zip -d /tmp/ && \
#     mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/ && \
#     chmod +x /usr/local/bin/chromedriver && \
#     rm -rf /tmp/*

# WORKDIR /app

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# CMD ["pytest", "-vv", "--junitxml=/workspace/report.xml"]

