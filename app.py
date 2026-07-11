from flask import Flask, render_template, request, jsonify
from user_manager import UserManager
from config_generator import generate_subscription, generate_vless_config, generate_vmess_config
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('admin.html')

@app.route('/api/users', methods=['GET'])
def get_users():
    users = UserManager.get_all_users()
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'protocol': u.protocol,
        'data_limit': u.data_limit,
        'used_traffic': u.used_traffic,
        'expiry_date': u.expiry_date.isoformat()
    } for u in users])

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    server_ip = request.headers.get('X-Forwarded-Host', 'localhost')
    
    user = UserManager.create_user(
        username=data['username'],
        protocol=data['protocol'],
        data_limit_gb=data['data_limit'] / 1e9,
        port=data['port'],
        expiry_days=30
    )
    
    if data['protocol'] == 'vless':
        config_link = generate_vless_config(user, server_ip, data['port'])
    else:
        config_link = generate_vmess_config(user, server_ip, data['port'])
    
    return jsonify({
        'status': 'created', 
        'id': user.id,
        'config_link': config_link
    })

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    UserManager.delete_user(user_id)
    return jsonify({'status': 'deleted'})

@app.route('/api/users/<int:user_id>/config')
def get_user_config(user_id):
    user = UserManager.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    server_ip = request.headers.get('X-Forwarded-Host', 'localhost')
    if user.protocol == 'vless':
        config_link = generate_vless_config(user, server_ip, user.port)
    else:
        config_link = generate_vmess_config(user, server_ip, user.port)
    return jsonify({'config_link': config_link})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
