from sqlalchemy import Column, Integer, DateTime, Numeric, CheckConstraint, Index
from sqlalchemy.orm import validates
from db import Base

class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    driver_id = Column(Integer, nullable=False, index=True)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    hourly_rate = Column(Numeric(10, 2), nullable=False)

    __table_args__ = (
        CheckConstraint("hourly_rate >= 0", name="ck_hourly_rate_nonneg"),
        Index("idx_driver_time", "driver_id", "start_time"),
    )

    @validates("hourly_rate")
    def _validate_rate(self, key, value):
        if value is None:
            raise ValueError("hourly_rate is required")
        if float(value) < 0:
            raise ValueError("hourly_rate must be non-negative")
        return value
