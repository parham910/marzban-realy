from models import User, engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import uuid

Session = sessionmaker(bind=engine)

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
        return user

    @staticmethod
    def get_user_by_username(username):
        session = Session()
        return session.query(User).filter_by(username=username).first()

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
