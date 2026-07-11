FROM python:3.9-slim

# نصب Xray و Nginx
RUN apt-get update && apt-get install -y wget unzip nginx && \
    wget https://github.com/XTLS/Xray-core/releases/latest/download/Xray-linux-64.zip && \
    unzip Xray-linux-64.zip -d /usr/local/bin/xray && \
    chmod +x /usr/local/bin/xray/xray && \
    rm Xray-linux-64.zip

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# کپی تنظیمات Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# اسکریپت start.sh
RUN echo '#!/bin/bash\n\
service nginx start\n\
/usr/local/bin/xray/xray run -c /app/xray_config.json &\n\
python app.py' > /app/start.sh && chmod +x /app/start.sh

CMD ["/app/start.sh"]
