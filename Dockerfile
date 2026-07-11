FROM python:3.9-slim

RUN apt-get update && apt-get install -y wget unzip nginx && \
    wget https://github.com/XTLS/Xray-core/releases/latest/download/Xray-linux-64.zip && \
    unzip Xray-linux-64.zip -d /usr/local/bin/xray && \
    chmod +x /usr/local/bin/xray/xray && \
    rm Xray-linux-64.zip

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

COPY nginx.conf /etc/nginx/nginx.conf

# اجرای مستقیم همه سرویس‌ها با یک خط
CMD ["sh", "-c", "service nginx start && /usr/local/bin/xray/xray run -c /app/xray_config.json & python app.py"]
