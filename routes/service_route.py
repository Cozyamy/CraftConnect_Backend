from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlmodel import Session, func, and_
from models.user_models import Service, Category, ServiceSchema
from dependencies.deps import get_db
from dependencies.deps import get_current_user
from models.user_models import User, Artisan
from controllers.service_controller import save_picture
from typing import List

service_router = APIRouter(tags=["Service"])

@service_router.post("/create_service/")
async def create_service(
    price: float = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    category_id: int = Form(...),
    picture_1: UploadFile = File(...),
    picture_2: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_premium and (picture_2 is not None):
        raise HTTPException(status_code=400, detail="Free plan allows only one picture")

    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        category = Category(name="New Category")
        db.add(category)
        db.commit()
        db.refresh(category) 

    artisan = db.query(Artisan).filter(Artisan.user_id == current_user.id).first()
    if not artisan:
        raise HTTPException(status_code=400, detail="Current user is not an artisan")

    picture_1_filename = save_picture(picture_1)
    picture_2_filename = save_picture(picture_2) if picture_2 else None

    db_service = Service(price=price, description=description, location=location, category_id=category.id, artisan_id=artisan.id, user_id=current_user.id, picture_1=picture_1_filename, picture_2=picture_2_filename)
    db.add(db_service)
    db.commit()
    db.refresh(db_service)

    return {"message": "Service created successfully"}

@service_router.get("/services")
async def get_all_services(db: Session = Depends(get_db)):
    db_services = db.query(Service).all()

    if not db_services:
        raise HTTPException(status_code=404, detail="No services found")

    return db_services

@service_router.get("/service/{service_id}")
async def get_service(service_id: int, db: Session = Depends(get_db)):
    db_service = db.query(Service).filter(Service.id == service_id).first()
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return db_service

@service_router.get("/user/services", response_model=List[ServiceSchema])
async def get_user_services(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_services = db.query(Service).filter(Service.user_id == current_user.id).all()
    if not user_services:
        raise HTTPException(status_code=404, detail="No services found for this user")
    return user_services

@service_router.get("/services")
async def get_services_by_category(category_name: str = None, db: Session = Depends(get_db)):
    if category_name:
        db_services = db.query(Service).join(Category).filter(func.lower(Category.name) == func.lower(category_name)).all()
    else:
        db_services = db.query(Service).all()

    if not db_services:
        raise HTTPException(status_code=404, detail="No services found")

    return db_services

@service_router.get("/services/category/{category_name}")
async def get_services_by_category(category_name: str, db: Session = Depends(get_db)):
    db_services = db.query(Service).join(Category).filter(func.lower(Category.name) == func.lower(category_name)).all()
    if not db_services:
        raise HTTPException(status_code=404, detail="No services found for this category")
    return db_services

@service_router.get("/services/search")
async def get_services_by_price_location_and_category(min_price: float = None, max_price: float = None, location: str = None, category_name: str = None, db: Session = Depends(get_db)):
    filters = []

    if min_price is not None:
        filters.append(Service.price >= min_price)
    if max_price is not None:
        filters.append(Service.price <= max_price)
    if location is not None:
        filters.append(Service.location == location)
    if category_name is not None:
        filters.append(func.lower(Category.name) == func.lower(category_name))
    if not filters:
        db_services = db.query(Service).all()
    else:
        db_services = db.query(Service).join(Category).filter(and_(*filters)).all()

    if not db_services:
        raise HTTPException(status_code=404, detail="No services found")

    return db_services

@service_router.put("/update_service/{service_id}")
async def update_service(
    service_id: int,
    price: float = Form(None),
    description: str = Form(None),
    location: str = Form(None),
    category_id: int = Form(None),
    picture_1: UploadFile = File(None),
    picture_2: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = db.query(Service).filter(Service.id == service_id, Service.user_id == current_user.id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    if price is not None:
        service.price = price
    if description is not None:
        service.description = description
    if location is not None:
        service.location = location
    if category_id is not None:
        service.category_id = category_id
    if picture_1 is not None:
        service.picture_1 = picture_1.filename
    if picture_2 is not None:
        service.picture_2 = picture_2.filename

    db.commit()
    return {"message": "Service updated successfully"}


@service_router.delete("/delete_service/{service_id}")
async def delete_service(service_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = db.query(Service).filter(Service.id == service_id, Service.user_id == current_user.id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found or not authorized to delete this service")

    db.delete(service)
    db.commit()

    return {"message": "Service deleted successfully"}