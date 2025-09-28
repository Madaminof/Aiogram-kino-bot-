from sqlalchemy import Column, Integer, String, BigInteger
from .db import Base

class Kino(Base):
    __tablename__ = "kino_izla"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    message_id = Column(BigInteger, nullable=False)
    file_id = Column(String, nullable=True)
