from sqlalchemy import Column, Integer, Float, DateTime
from db import Base

class Delivery(Base):
    """
    Delivery model representing a single delivery session by a driver.

    Attributes:
        id (int): Primary key, auto-incremented.
        driver_id (int): ID of the driver associated with the delivery.
        start_time (datetime): Delivery start timestamp.
        end_time (datetime): Delivery end timestamp.
        hourly_rate (float): Hourly payment rate for the driver.
    """
    __tablename__ = "deliveries"

    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, nullable=False, index=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    hourly_rate = Column(Float, nullable=False)
