from fastapi import Form, UploadFile, HTTPException
from models.user_models import ArtisanIn
import os
import uuid

def parse_artisan_info(address: str = Form(...)) -> ArtisanIn:
    return ArtisanIn(address=address)

def validate_artisan_info(artisan_info: ArtisanIn):
    if not artisan_info.address:
        raise HTTPException(status_code=400, detail="Please provide all required information.")

def validate_picture(picture: UploadFile):
    if not picture.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        raise HTTPException(status_code=400, detail="Please upload a picture in JPEG, JPG or PNG format.")

def save_picture(picture: UploadFile):
    contents = picture.file.read()
    if len(contents) > 10 * 1024 * 1024:  # 10 MB limit
        raise HTTPException(status_code=400, detail="File size exceeds limit (10MB).")

    file_extension = picture.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    upload_folder = "./uploaded_images"
    file_path = os.path.join(upload_folder, unique_filename)

    os.makedirs(upload_folder, exist_ok=True)
    with open(file_path, "wb") as file_object:
        file_object.write(contents)
    
    return unique_filename 