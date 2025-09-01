FROM python:3.13-slim-bookworm

# Instalar dependências do Linux
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg fonts-liberation libasound2 libatk1.0-0 \
    libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 libnspr4 libnss3 \
    libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 xdg-utils \
    netcat-traditional --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Instalar Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Instalar UV Astral
COPY --from=ghcr.io/astral-sh/uv:0.7.20 /uv /uvx /usr/local/bin/

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependência do UV
COPY pyproject.toml uv.lock /app/
RUN uv sync --locked

# Copiar restante do código
COPY . /app

# Comando padrão usando UV
CMD ["uv", "run", "uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
