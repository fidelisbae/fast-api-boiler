from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(String(100), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(100), unique=True, nullable=False)
    cash = Column(Integer, nullable=False)

    devices = relationship("Device", back_populates="user")
