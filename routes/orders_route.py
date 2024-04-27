from fastapi import APIRouter, Depends, HTTPException, Form
from sqlmodel import Session
from models.user_models import User, Order, Artisan, Booking
from dependencies.deps import get_db, get_current_user

order_router = APIRouter(tags=["Orders"])

@order_router.get("/user_orders")
async def get_user_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    orders = db.query(Order, Artisan, User, Booking).\
        join(Artisan, Order.artisan_id == Artisan.id).\
        join(User, Artisan.user_id == User.id).\
        join(Booking, Order.service_id == Booking.service_id).\
        filter(Order.user_id == current_user.id).all()
    
    result = []
    for order, artisan, user, booking in orders:
        result.append({
            "order_id": order.id,
            "name": f"{user.first_name} {user.last_name}",
            "service_booked": booking.workdetails,
            "phone_number": user.phone_number,
            "date": order.date,
            "status": order.status
        })
    
    return result

@order_router.get("/artisan_orders")
async def get_artisan_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    orders = db.query(Order, User, Booking).\
        join(User, Order.user_id == User.id).\
        join(Booking, Order.service_id == Booking.service_id).\
        filter(Order.artisan_id == current_user.id).all()
    
    result = []
    for order, user, booking in orders:
        result.append({
            "order_id": order.id,
            "name": f"{user.first_name} {user.last_name}",
            "service_booked": booking.workdetails,
            "phone_number": user.phone_number,
            "date": order.date,
            "status": order.status
        })
    
    return result

@order_router.put("/user_update_order_status/{order_id}")
async def user_update_order_status(order_id: int, status: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    if status not in ["cancelled", "completed"]:
        raise HTTPException(status_code=400, detail="Invalid status update")

    db_order.status = "declined" if status == "cancelled" else "delivered"
    db.commit()
    return {"message": "Order status updated successfully"}

@order_router.put("/artisan_update_order_status/{order_id}")
async def artisan_update_order_status(order_id: int, status: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_order = db.query(Order).filter(Order.id == order_id, Order.artisan_id == current_user.id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    if status not in ["declined", "delivered"]:
        raise HTTPException(status_code=400, detail="Invalid status update")

    db_order.status = "cancelled" if status == "declined" else "completed"
    db.commit()
    return {"message": "Order status updated successfully"}