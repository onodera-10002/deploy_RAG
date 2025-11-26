from sqlalchemy import Column, Integer, String, Text, DateTime, func
from api.db import Base

class Message(Base):
     __tablename__ = "messages"
     # カラムの定義
     id = Column(Integer, primary_key = True, index = True)
     session_id = Column(String(255), index = True)
     role = Column(String(50))
     content = Column(Text)
     created_at = Column(DateTime(timezone = True), server_default = func.now())



