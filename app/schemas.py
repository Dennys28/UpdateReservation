from pydantic import BaseModel
import datetime

class ReservationCreate(BaseModel):
    customer_id: int
    table_id: int
    restaurant_id: int
    reservation_time: datetime.datetime

class ReservationResponse(ReservationCreate):
    id: int
    status: str

    class Config:
        from_attributes = True
