
FROM python:3.9-slim

WORKDIR /scrapping

COPY . .
# Defina o frontend do APT para não interativo
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependências necessárias
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libnspr4 \
    libnss3 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    lsb-release  # Adicionando o lsb-release para verificar a versão do Ubuntu

# Adicionar a chave do Google Chrome e configurar o repositório
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && apt-get install -y google-chrome-stable
# Atualizar o apt e instalar o Google Chrome
RUN apt-get update && apt-get install -y google-chrome-stable

RUN pip install -r requirements.txt

CMD ["python3", "scrapping.py"]
