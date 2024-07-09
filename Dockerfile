# Use uma imagem base do Ubuntu 20.04
FROM ubuntu:20.04

# Defina o diretório de trabalho
WORKDIR /wrapping

# Copie o conteúdo do diretório atual para o diretório de trabalho no contêiner
COPY . .

# Defina o frontend do APT para não interativo
ENV DEBIAN_FRONTEND=noninteractive

# Atualize a lista de pacotes e instale as dependências
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    python3 \
    python3-pip \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Adicione o repositório do Google Chrome e instale o Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && apt-get install -y google-chrome-stable

# Verifique a versão do Google Chrome
RUN google-chrome --version

# Baixe e instale uma versão específica do ChromeDriver
RUN wget -q "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip" && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm chromedriver_linux64.zip

# Instale as dependências do Python
RUN pip3 install --no-cache-dir -r requirements.txt

# Defina o ponto de entrada do contêiner. Modifique conforme necessário.
CMD ["python3", "scrapping.py"]
