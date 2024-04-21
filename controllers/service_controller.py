from fastapi import UploadFile, HTTPException
from controllers.artisan_controller import validate_picture
import os
import uuid

def save_picture(picture: UploadFile):
    validate_picture(picture)
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