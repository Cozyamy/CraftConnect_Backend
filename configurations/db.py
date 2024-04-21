import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred)

from sqlmodel import create_engine

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)