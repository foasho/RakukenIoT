from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"mysql_collate": "utf8_general_ci"}
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True)
    email = Column(String(255), unique=True, index=True)
    line_id = Column(String(255), default=None, nullable=True)
    line_connect_code = Column(String(255), nullable=True, default=None)
    password = Column(String(255))
    topper = Column(Integer, default=None, nullable=True)
    refresh_token = Column(Text, default=None, nullable=True)
    is_active = Column(Boolean, default=True)

# 体重ログ
class WeightLog(Base):
    __tablename__ = "weight_logs"
    __table_args__ = {"mysql_collate": "utf8_general_ci"}
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")
    value = Column(Float)
    memo = Column(Text, nullable=True, default=None)
    other = Column(String(255), nullable=True, default=None)
    created_at = Column(DateTime, default=datetime.now)