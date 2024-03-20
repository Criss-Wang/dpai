from sqlalchemy.orm import Session

from .models import MLModel
from typing import List


def get_ml_model(db: Session, model_name: str) -> MLModel | None:
    return db.query(MLModel).filter(MLModel.name == model_name).first()


def get_all_models(db: Session) -> List[MLModel]:
    return db.query(MLModel).all()


def create_ml_model(
    db: Session, model_name: str, model_path: str, inference_path: str
) -> None:
    db_model = MLModel(
        name=model_name,
        model_path=model_path,
        inference_path=inference_path,
    )
    db.add(db_model)
    db.commit()
    db.refresh(db_model)


# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()

# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
