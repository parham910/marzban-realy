from flask import Flask, render_template, request, jsonify
from user_manager import UserManager
from config_generator import generate_subscription
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
    user = UserManager.create_user(
        username=data['username'],
        protocol=data['protocol'],
        data_limit_gb=data['data_limit'] / 1e9,
        port=data['port'],
        expiry_days=30
    )
    return jsonify({'status': 'created', 'id': user.id})

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    UserManager.delete_user(user_id)
    return jsonify({'status': 'deleted'})

@app.route('/sub/<username>')
def get_sub(username):
    user = UserManager.get_user_by_username(username)
    if not user:
        return "User not found", 404
    # تولید ساب‌لینک برای این کاربر
    sub_text = f"vless://{user.uuid}@example.com:{user.port}?..."
    return sub_text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
