from typing import Generator
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, Session

from dpai.model_db.models import Base, MLModel
from dpai.model_db.crud import get_ml_model, get_all_models, create_ml_model

import pytest


DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    database = TestingSessionLocal()
    yield database
    database.close()


@pytest.fixture
def db_item():
    return MLModel(id=1, name="test_model", model_path="", inference_path="")


@pytest.fixture
def db_session(db_item) -> Generator[Session, None, None]:
    # Create an in-memory SQLite database for testing
    Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()

    db_session.add(db_item)
    db_session.commit()

    yield db_session

    # Tear down the database after testing
    db_session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.mark.parametrize("model_name", [("test_model")])
def test_get_ml_model_existing_model(db_session, model_name, db_item):
    # Create a mock MLModel object in the database
    result = get_ml_model(db_session, model_name)

    # Assert that the returned MLModel object matches the one created
    assert result.id == db_item.id
    assert result.name == db_item.name
    assert result.model_path == db_item.model_path
    assert result.inference_path == db_item.inference_path


@pytest.mark.parametrize("model_name", [("nonexistent_model")])
def test_get_ml_model_nonexistent_model(db_session, model_name):
    # Call the function under test with a model name that doesn't exist
    result = get_ml_model(db_session, model_name)

    assert result is None


def test_get_all_models(db_session, db_item):
    result = get_all_models(db_session)
    assert len(result) == 1
    assert result[0].id == db_item.id
    assert result[0].name == db_item.name
    assert result[0].model_path == db_item.model_path
    assert result[0].inference_path == db_item.inference_path


def test_create_ml_model(db_session):
    # Call the function under test to create a new MLModel
    model_name = "new_model"
    model_path = "/path/to/model"
    inference_path = "/path/to/inference"
    create_ml_model(db_session, model_name, model_path, inference_path)

    # Query the database to get the created MLModel
    db_model = db_session.query(MLModel).filter_by(name=model_name).first()

    # Assert that the created MLModel matches the expected values
    assert db_model is not None
    assert db_model.name == model_name
    assert db_model.model_path == model_path
    assert db_model.inference_path == inference_path
