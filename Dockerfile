FROM python:3.9-slim

# نصب Xray
RUN apt-get update && apt-get install -y wget unzip && \
    wget https://github.com/XTLS/Xray-core/releases/latest/download/Xray-linux-64.zip && \
    unzip Xray-linux-64.zip -d /usr/local/bin/xray && \
    chmod +x /usr/local/bin/xray/xray && \
    rm Xray-linux-64.zip

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# اجرای Xray و Flask
RUN echo '#!/bin/bash\n/usr/local/bin/xray/xray run -c /app/xray_config.json &\npython app.py' > /app/start.sh && chmod +x /app/start.sh

CMD ["/app/start.sh"]
