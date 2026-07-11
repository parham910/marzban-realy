from flask import Flask, render_template, request, jsonify
from user_manager import UserManager
from config_generator import generate_vless_config, generate_vmess_config
import json

app = Flask(__name__)

# ... بقیه کدها مثل قبل ...

if __name__ == '__main__':
    # تغییر پورت به 8081
    app.run(host='0.0.0.0', port=8081)
