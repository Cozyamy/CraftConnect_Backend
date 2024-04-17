import os

import firebase_admin
from firebase_admin import credentials
from sqlmodel import Session, SQLModel, create_engine

from utils import load_json_into_dict

file_name: str = "database.sqlite"
file_dir: str = "assets"


# init firebase
firebase_secret = os.path.join("env", "firebase-secret.json")
firebase_credentials = credentials.Certificate(load_json_into_dict(firebase_secret))
firebase_admin.initialize_app(credential=firebase_credentials)


# file path of db asset
file_path: str = os.path.join(file_dir, file_name)

# create folder if it does not exist
if not os.path.exists(file_dir):
    os.makedirs(file_dir)


db_url: str = f"sqlite:///{file_path}"

# create or connect to db
engine = create_engine(url=db_url, echo=True)
