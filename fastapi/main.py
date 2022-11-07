from typing import Union

from fastapi import FastAPI, HTTPException
import logging

from joblib import load
import numpy as np
from datetime import datetime

logging.config.fileConfig('logging.conf', disable_existing_loggers=True)
logger = logging.getLogger(__name__)

app = FastAPI(debug = True)

model = load('svc.joblib')
scaler = load('scaler.joblib')

PARAMS_NAMES = {
    0: 'speal_length',
    1: 'speal_width',
    2: 'petal_length',
    3: 'petal_width'
}
CLASS_NAMES = {
    0: 'setosa',
    1: 'versicolor',
    2: 'virginica'
}


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/predict/")
def predict(speal_length: float = None, speal_width: float = None, petal_length: float = None, petal_width: float = None):
    
    X = np.array([[speal_length, speal_width, petal_length, petal_width]])
    
    if None in X[0]:
        not_specified = [PARAMS_NAMES[idx] for idx, param in enumerate(X[0]) if param is None]
        logger.error(f"The following parameters aren't specified: {not_specified}")
        raise HTTPException(status_code=404, detail=f"Please specify the following parameters: {not_specified}")

    start = datetime.now()
    X_scaled = scaler.transform(X)
    y = model.predict(X_scaled)[0]
    end = datetime.now()
    
    time = end - start

    logger.info(f"Time used for inference: {time}")

    return {"prediction": CLASS_NAMES[y]}
