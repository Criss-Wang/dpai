from typing import List
from contextlib import asynccontextmanager

from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .utils import run_inference
from .model_db.crud import get_ml_model
from .model_db.db_setup import Base, SessionLocal, engine


class Input(BaseModel):
    data: List[str]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    Base.metadata.create_all(bind=engine)
    yield
    # shutdown
    Base.metadata.drop_all(bind=engine)


app = FastAPI(lifespan=lifespan)


# Dependency to get the database session, ignored during test
def get_db():  # pragma: no cover
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/{model_name}/predict")
async def predict(model_name: str, request_body: Input, db: Session = Depends(get_db)):
    model = get_ml_model(db, model_name)
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid model name, this model is not in registry",
        )

    model_path, inference_path = model.model_path or "", model.inference_path or ""

    try:
        result = run_inference(request_body.data, model_path, inference_path)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error running inference, check your inference script. Error: {str(e)}",
        )
    if isinstance(result, str):
        return {"response": result}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Response format is not string, check your inference file's predict_fn again",
        )
