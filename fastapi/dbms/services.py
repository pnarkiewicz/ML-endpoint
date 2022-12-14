from dbms import database, schemas, models
from typing import List
from sqlalchemy import func


def add_tables():
    return database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def add_request(request: schemas.BaseGetRequests, db) -> schemas.BaseGetRequests:
    request = models.GetRequests(**request.dict())

    db.add(request)
    db.commit()
    db.refresh(request)

    return schemas.BaseGetRequests.from_orm(request)


def get_all_requests(db) -> List[schemas.BaseGetRequests]:
    return db.query(models.GetRequests).all()


def get_index(db):
    current_index = db.query(func.max(models.GetRequests.index)).one()[0]

    if type(current_index) == int:
        return current_index + 1
    else:
        return 0
