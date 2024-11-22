# class User:
#     def __init__(self, username: str, hashed_password: str, secret_key: str):
#         self.username = username
#         self.hashed_password = hashed_password
#         self.secret_key = secret_key

from sqlalchemy import Column, Integer, String
from db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    secret_key = Column(String, nullable=False) 