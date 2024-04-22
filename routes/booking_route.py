from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
# from models.user_models import Service, User, Booking, BookingCreate
from dependencies.deps import get_db, get_current_user

booking_router = APIRouter(tags=["Booking"])

# @booking_router.post("/bookings/")
# def create_booking(booking: BookingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     db_service = db.query(Service).filter(Service.id == booking.service_id).first()
#     if not db_service:
#         raise HTTPException(status_code=404, detail="Service not found")

#     db_user = db.query(User).filter(User.id == current_user.id).first()
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")

#     if booking.name is not None:
#         db_user.name = booking.name
#     if booking.email is not None:
#         db_user.email = booking.email
#     if booking.phone_number is not None:
#         db_user.phone_number = booking.phone_number

#     db_booking = Booking(**booking.dict(exclude={"name", "email", "phone_number"}), user=db_user, service=db_service)
#     db.add(db_booking)
#     db.commit()
#     db.refresh(db_booking)
#     return db_booking