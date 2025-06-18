from sqlalchemy import Column, Float, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship


class Device(Base):
    __tablename__ = "device"

    id = Column(String(100), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(100), nullable=False)
    temperature_upper_limit = Column(Float, nullable=False)
    temperature_lower_limit = Column(Float, nullable=False)
    humidity_upper_limit = Column(Float, nullable=False)
    humidity_lower_limit = Column(Float, nullable=False)
    alarm_frequency_minutes = Column(Integer, nullable=False)
    user_id = Column(String(100), nullable=False)
    user = relationship("User", back_populates="devices")
