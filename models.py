from sqlalchemy import create_engine, Column, Integer, String, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()
engine = create_engine('sqlite:///users.db')

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    uuid = Column(String)
    data_limit = Column(BigInteger)
    used_traffic = Column(BigInteger, default=0)
    expiry_date = Column(DateTime)
    protocol = Column(String)
    port = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Integer, default=1)

Base.metadata.create_all(engine)
