from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
import pytest

from dpai.fastapi_main import app, Base, get_db

# Setup the TestClient
client = TestClient(app)

# Setup the in-memory SQLite database for testing
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to override the get_db dependency in the main app
def override_get_db():
    database = TestingSessionLocal()
    yield database
    database.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def test_app():
    with TestClient(app) as client:
        yield client


def test_root(test_app):
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@patch("dpai.fastapi_main.run_inference")
@patch("dpai.fastapi_main.get_ml_model")
def test_predict_success(mock_get_ml_model, mock_run_inference, test_app):
    # Mock get_ml_model to return model paths
    mock_get_ml_model.return_value = Mock(
        model_path="mock_path", inference_path="mock_path"
    )

    # Mock run_inference to return a string response
    mock_run_inference.return_value = "Prediction result"

    response = test_app.post("/mock_model/predict", json={"data": ["example_data"]})

    mock_run_inference.assert_called_once_with(
        ["example_data"], "mock_path", "mock_path"
    )
    assert response.status_code == 200
    assert response.json() == {"response": "Prediction result"}


@patch("dpai.fastapi_main.run_inference")
@patch("dpai.fastapi_main.get_ml_model")
def test_predict_invalid_model(mock_get_ml_model, mock_run_inference, test_app):
    # Failed model retrieval
    mock_get_ml_model.return_value = None
    response = test_app.post("/mock_model/predict", json={"data": ["example_data"]})

    mock_run_inference.assert_not_called()
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid model name, this model is not in registry"
    }


@patch("dpai.fastapi_main.run_inference")
@patch("dpai.fastapi_main.get_ml_model")
def test_predict_invalid_inference_result(
    mock_get_ml_model, mock_run_inference, test_app
):
    # inference result is problematic
    mock_get_ml_model.return_value = Mock(
        model_path="mock_path", inference_path="mock_path"
    )
    mock_run_inference.return_value = {"result": "not_a_string"}

    response = test_app.post("/mock_model/predict", json={"data": ["example_data"]})

    mock_run_inference.assert_called_once_with(
        ["example_data"], "mock_path", "mock_path"
    )
    assert response.status_code == 500
    assert response.json() == {
        "detail": "Response format is not string, check your inference file's predict_fn again"
    }


@patch("dpai.fastapi_main.run_inference")
@patch("dpai.fastapi_main.get_ml_model")
def test_predict_inference_error(mock_get_ml_model, mock_run_inference, test_app):
    # inference result is problematic
    mock_get_ml_model.return_value = Mock(
        model_path="mock_path", inference_path="mock_path"
    )
    mock_run_inference.side_effect = Exception("error message")
    response = test_app.post("/mock_model/predict", json={"data": ["example_data"]})

    mock_run_inference.assert_called_once_with(
        ["example_data"], "mock_path", "mock_path"
    )
    assert response.status_code == 500
    assert response.json() == {
        "detail": "Error running inference, check your inference script. Error: error message"
    }


def setup() -> None:
    # Create the tables in the test database
    Base.metadata.create_all(bind=engine)


def teardown() -> None:
    # Drop the tables in the test database
    Base.metadata.drop_all(bind=engine)
