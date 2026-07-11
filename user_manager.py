from models import User, engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import uuid
import json
import os

Session = sessionmaker(bind=engine)
XRAY_CONFIG = "/app/xray_config.json"

class UserManager:
    @staticmethod
    def create_user(username, protocol, data_limit_gb, port, expiry_days=30):
        session = Session()
        user = User(
            username=username,
            uuid=str(uuid.uuid4()),
            data_limit=int(data_limit_gb * 1e9),
            port=port,
            protocol=protocol,
            expiry_date=datetime.utcnow() + timedelta(days=expiry_days)
        )
        session.add(user)
        session.commit()
        UserManager.add_user_to_xray(user)
        return user

    @staticmethod
    def add_user_to_xray(user):
        if not os.path.exists(XRAY_CONFIG):
            return False
        with open(XRAY_CONFIG, 'r') as f:
            config = json.load(f)
        new_client = {
            "id": user.uuid,
            "flow": "xtls-rprx-vision",
            "email": user.username
        }
        config["inbounds"][0]["settings"]["clients"].append(new_client)
        with open(XRAY_CONFIG, 'w') as f:
            json.dump(config, f, indent=2)
        return True

    @staticmethod
    def get_user_by_username(username):
        session = Session()
        return session.query(User).filter_by(username=username).first()

    @staticmethod
    def get_user_by_id(user_id):
        session = Session()
        return session.query(User).filter_by(id=user_id).first()

    @staticmethod
    def get_all_users():
        session = Session()
        return session.query(User).all()

    @staticmethod
    def delete_user(user_id):
        session = Session()
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            session.delete(user)
            session.commit()
            return True
        return False
