from sqlalchemy import Column, Integer, String

from .db_setup import Base


class MLModel(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    model_path = Column(String, nullable=False)
    inference_path = Column(String, nullable=False)
