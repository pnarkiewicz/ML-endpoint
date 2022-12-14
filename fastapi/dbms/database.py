import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext import declarative
from dotenv import load_dotenv

load_dotenv()

user = os.environ.get("POSTGRES_USER")
password = os.environ.get("POSTGRES_PASSWORD")
server = os.environ.get("POSTGRES_SERVER")
db_name = os.environ.get("POSTGRES_DB")

DATABASEURL = f"postgresql://{user}:{password}@{server}/{db_name}"

engine = create_engine(DATABASEURL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative.declarative_base()
