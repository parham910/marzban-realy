import uuid
import json
import base64

def generate_vless_config(user, server_ip, port):
    return f"vless://{user.uuid}@{server_ip}:{port}?encryption=none&security=tls&sni={server_ip}&fp=chrome&type=ws&path=%2F#{user.username}"

def generate_vmess_config(user, server_ip, port):
    config = {
        "v": "2",
        "ps": user.username,
        "add": server_ip,
        "port": port,
        "id": user.uuid,
        "aid": "0",
        "net": "ws",
        "type": "none",
        "host": "",
        "path": "/",
        "tls": "tls"
    }
    config_json = json.dumps(config, separators=(',', ':'))
    return f"vmess://{base64.b64encode(config_json.encode()).decode()}"

def generate_subscription(users, server_ip):
    links = []
    for user in users:
        if user.protocol == "vless":
            links.append(generate_vless_config(user, server_ip, user.port))
        elif user.protocol == "vmess":
            links.append(generate_vmess_config(user, server_ip, user.port))
    return base64.b64encode("\n".join(links).encode()).decode()
