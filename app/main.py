from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from models import Reservation
from schemas import ReservationCreate, ReservationResponse

# Inicializar la base de datos
init_db()

# Crear instancia de FastAPI
app = FastAPI(title="Reservation Service", description="Microservicio para la gestión de reservas", version="1.0")


# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Reservation Service is running"}


@app.post("/create_reservation/", response_model=ReservationResponse)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    new_reservation = Reservation(**reservation.dict(), status="Confirmed")
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    return new_reservation


@app.put("/update_reservation/{reservation_id}")
def update_reservation(reservation_id: int, status: str, db: Session = Depends(get_db)):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    reservation.status = status
    db.commit()
    return {"message": f"Reservation {reservation_id} updated to {status}"}


@app.get("/reservation/{reservation_id}", response_model=ReservationResponse)
def get_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation


@app.delete("/delete_reservation/{reservation_id}")
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    db.delete(reservation)
    db.commit()
    return {"message": f"Reservation {reservation_id} deleted"}
