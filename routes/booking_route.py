from fastapi import APIRouter, Depends, HTTPException, Form
from sqlmodel import Session
from models.user_models import Service, User, Booking, Order
from dependencies.deps import get_db, get_current_user
from typing import Optional
from datetime import datetime

booking_router = APIRouter(tags=["Booking"])

@booking_router.post("/create_booking/{service_id}")
async def create_booking(
    service_id: int,
    first_name: Optional[str] = Form(None),
    last_name: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    phone_number: Optional[str] = Form(None),
    workdetails: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ Create a new booking """
    db_service = db.query(Service).filter(Service.id == service_id).first()
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    first_name = first_name or current_user.first_name
    last_name = last_name or current_user.last_name
    email = email or current_user.email
    phone_number = phone_number or current_user.phone_number
    
    name = f"{first_name} {last_name}"
    
    db_booking = Booking(
        service_id=service_id,
        user_id=current_user.id,
        name=name,
        email=email,
        phone_number=phone_number,
        workdetails=workdetails,
        time=datetime.now()
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)

    # Create an Order record
    db_order = Order(
        user_id=current_user.id,
        artisan_id=db_service.artisan_id,
        service_id=service_id,
        status="PENDING",
        date=datetime.now()
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    service_user = db_service.user
    service_user_details = {
        "first_name": service_user.first_name,
        "last_name": service_user.last_name,
        "phone_number": service_user.phone_number,
        "profile_picture": service_user.profile_picture
    }

    return {
        "message": "Booking created successfully",
        "service_user_details": service_user_details
    }