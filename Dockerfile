FROM python:3.9-slim

# نصب Xray
RUN apt-get update && apt-get install -y wget unzip && \
    wget -qO /tmp/Xray-linux-64.zip https://github.com/XTLS/Xray-core/releases/latest/download/Xray-linux-64.zip && \
    unzip /tmp/Xray-linux-64.zip -d /usr/local/bin/xray && \
    chmod +x /usr/local/bin/xray/xray && \
    rm /tmp/Xray-linux-64.zip

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# اجرای Xray در پس‌زمینه و سپس Flask
CMD ["sh", "-c", "/usr/local/bin/xray/xray run -c /app/xray_config.json > /app/xray.log 2>&1 & python app.py"]
