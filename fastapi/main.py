from typing import Union

from fastapi import FastAPI, HTTPException
import logging
from fastapi.logger import logger as fastapi_logger

from joblib import load
import numpy as np
from datetime import datetime
from dbms import services, schemas, database

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

app = FastAPI(debug=True)
db = database.SessionLocal()
services.add_tables()

model = load("models/svc.joblib")
scaler = load("models/scaler.joblib")

PARAMS_NAMES = {
    0: "speal_length",
    1: "speal_width",
    2: "petal_length",
    3: "petal_width",
}

CLASS_NAMES = {0: "setosa", 1: "versicolor", 2: "virginica"}


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/predict/")
def predict(
    speal_length: float = None,
    speal_width: float = None,
    petal_length: float = None,
    petal_width: float = None,
):

    X = np.array([[speal_length, speal_width, petal_length, petal_width]])
    logger.info(X)

    incorrect = [
        PARAMS_NAMES[idx]
        for idx, param in enumerate(X[0])
        if isinstance(param, float) == False
    ]

    # I.e. there are any incorrect parameters
    if len(incorrect) > 0:
        logger.error(
            f"The following parameters aren incorrectly specified: {incorrect}"
        )
        start = datetime.now()
        log = {
            "index": services.get_index(db),
            "date": start,
            "speal_width": speal_width,
            "speal_length": speal_length,
            "petal_width": petal_width,
            "petal_length": petal_length,
            "message": f"The following parameters aren incorrectly specified: {incorrect}",
        }
        request = schemas.BaseGetRequests(**log)
        services.add_request(request, db)
        raise HTTPException(
            status_code=404,
            detail=f"Please specify the following parameters: {incorrect}",
        )

    start = datetime.now()
    X_scaled = scaler.transform(X)
    y = model.predict(X_scaled)[0]
    end = datetime.now()

    time = end - start

    logger.info(f"\nTime used for inference: {time}")

    log = {
        "index": services.get_index(db),
        "date": start,
        "speal_width": speal_width,
        "speal_length": speal_length,
        "petal_width": petal_width,
        "petal_length": petal_length,
        "message": CLASS_NAMES[y],
    }

    request = schemas.BaseGetRequests(**log)
    services.add_request(request, db)

    return {"prediction": CLASS_NAMES[y]}


@app.get("/get_requests")
def get_requests():
    return services.get_all_requests(db)
