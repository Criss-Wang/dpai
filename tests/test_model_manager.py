from unittest.mock import patch, Mock
import pytest
from dpai.model_manager import ModelManager, ModelException


@pytest.fixture
def mock_session():
    with patch("dpai.model_manager.SessionLocal") as mock_session:
        yield mock_session.return_value


@patch("dpai.model_manager.create_ml_model")
@patch("dpai.model_manager.get_ml_model")
def test_register_model_existing_model(
    mock_get_ml_model, mock_create_ml_model, mock_session
):
    # Mock get_ml_model to return a non-None value, indicating an existing model
    mock_get_ml_model.return_value = Mock()

    model_manager = ModelManager()

    # Assert that ModelException is raised
    with pytest.raises(ModelException) as exc_info:
        model_manager.register_model("existing_model", "model_path", "inference_path")

    mock_get_ml_model.assert_called_once_with(mock_session, "existing_model")
    mock_create_ml_model.assert_not_called()
    assert "Model with the same already register" in str(exc_info.value)


@patch("dpai.model_manager.create_ml_model")
@patch("dpai.model_manager.get_ml_model")
def test_register_model_new_model(
    mock_get_ml_model, mock_create_ml_model, mock_session
):
    # Mock get_ml_model to return None, indicating a new model
    mock_get_ml_model.return_value = None

    model_manager = ModelManager()

    # Call the function under test
    model_manager.register_model("new_model", "model_path", "inference_path")

    mock_get_ml_model.assert_called_once_with(mock_session, "new_model")
    mock_create_ml_model.assert_called_once_with(
        mock_session, "new_model", "model_path", "inference_path"
    )


@patch("dpai.model_manager.get_all_models")
def test_load_models(mock_get_all_models, mock_session):
    # Mock get_all_models to return some mock models
    mock_model_1 = Mock()
    mock_model_2 = Mock()
    mock_get_all_models.return_value = [mock_model_1, mock_model_2]

    model_manager = ModelManager()

    # Call the function under test
    model_manager.load_models()

    # Assertions
    assert len(model_manager._ModelManager__models) == 2  # Check if models are loaded
    mock_get_all_models.assert_called_once_with(
        mock_session
    )  # Check if get_all_models is called


@patch("dpai.model_manager.get_all_models")
def test_load_models_with_exception(mock_get_all_models, mock_session):
    # Mock get_all_models to return some mock models
    model_manager = ModelManager()

    mock_get_all_models.side_effect = Exception()
    with pytest.raises(ModelException) as exc_info:
        _ = model_manager.load_models()

    # Assertions
    assert "Cannot get models from db" in str(exc_info.value)
    mock_get_all_models.assert_called_once_with(
        mock_session
    )  # Check if get_all_models is called
