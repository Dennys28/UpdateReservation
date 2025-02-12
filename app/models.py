from sqlalchemy import Column, Integer, String, DateTime
from database import Base
import datetime

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True, unique=True)  # 🔹 Explicitamente único
    customer_id = Column(Integer, nullable=False)  # 🔹 No debe ser NULL
    table_id = Column(Integer, nullable=False)  # 🔹 No debe ser NULL
    restaurant_id = Column(Integer, nullable=False)  # 🔹 No debe ser NULL
    reservation_time = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)  # 🔹 No NULL
    status = Column(String(50), default="Pending", nullable=False)  # 🔹 No NULL

    def __repr__(self):
        return f"<Reservation {self.id} - Customer {self.customer_id} - Status {self.status}>"
