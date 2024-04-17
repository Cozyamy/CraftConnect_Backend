from sqlmodel import Session, SQLModel, create_engine
import os

file_name: str = "database.sqlite"
file_dir: str = "assets"

# file path of db asset
file_path: str = os.path.join(file_dir, file_name)

# create folder if it does not exist
if not os.path.exists(file_dir):
    os.makedirs(file_dir)


db_url: str = f"sqlite:///{file_path}"

# create or connect to db
engine = create_engine(url=db_url)
