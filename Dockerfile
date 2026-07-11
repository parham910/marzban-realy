FROM python:3.9-slim

RUN apt-get update && apt-get install -y wget unzip && \
    wget -qO /tmp/xray.zip https://github.com/XTLS/Xray-core/releases/latest/download/Xray-linux-64.zip && \
    unzip /tmp/xray.zip -d /usr/local/bin/xray && \
    chmod +x /usr/local/bin/xray/xray

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["sh", "-c", "/usr/local/bin/xray/xray run -c /app/xray_config.json & python app.py"]
