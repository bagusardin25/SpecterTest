# SpecterTest Backend — Python 3.12 + Playwright
FROM python:3.12-slim

# System dependencies for Playwright
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir \
    flask>=3.1.1 \
    flask-cors>=5.0.0 \
    flask-sqlalchemy>=3.0.5 \
    playwright>=1.51.0 \
    openai>=1.60.0 \
    python-dotenv>=1.0.0

# Install Playwright Chromium
RUN playwright install chromium

# Copy application code
COPY . .

EXPOSE 5001

CMD ["python", "run.py"]
