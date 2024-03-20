import os
import pytest
from unittest.mock import Mock, patch
from dpai import (
    run_inference,
    start_app,
)
from dpai.model_manager import InferenceException


dir_path = os.path.dirname(os.path.realpath(__file__))


class TestUtils:
    @pytest.fixture(autouse=True)
    def init_model(self):
        self._model_name = "mock_model_name"
        self._inference_path = "mock_inference_path"
        self._model_path = "mock_model_path"
        self._specs = {}
        self._port = 9000
        self._model_manager = Mock()

    @pytest.mark.parametrize(
        "data, expected", [({"data": "mock_data"}, "prediction_result")]
    )
    @patch("importlib.util.spec_from_file_location")
    @patch("importlib.util.module_from_spec")
    @patch("dpai.utils.load")
    def test_run_inference(
        self,
        mock_load,
        mock_module_from_spec,
        mock_spec_from_file_location,
        data,
        expected,
    ):
        mock_spec_from_file_location.return_value = Mock()
        mock_inference_file = Mock()
        mock_module_from_spec.return_value = mock_inference_file
        mock_load.return_value = {"model": Mock()}

        # TEST 1: error transforming input
        mock_inference_file.input_fn.side_effect = Exception("Input Function Error")

        with pytest.raises(InferenceException) as exc_info:
            result = run_inference(data, self._model_path, self._inference_path)
        mock_load.assert_called_once_with(self._model_path)
        mock_inference_file.input_fn.assert_called_once_with(data)
        mock_inference_file.predict_fn.assert_not_called()
        assert "Failed to load data" in str(exc_info.value)

        # TEST 2: error during inference
        mock_inference_file.input_fn.side_effect = None  # Reset side effect
        mock_inference_file.input_fn.return_value = Mock()
        mock_inference_file.predict_fn.side_effect = Exception("Predict Function Error")

        with pytest.raises(InferenceException) as exc_info:
            result = run_inference(data, self._model_path, self._inference_path)
        mock_inference_file.predict_fn.assert_called_once_with(
            mock_inference_file.input_fn.return_value, mock_load.return_value["model"]
        )
        assert "Failed to run inference" in str(exc_info.value)

        # Test 3: successful run
        mock_inference_file.predict_fn.side_effect = None
        mock_inference_file.predict_fn.return_value = "prediction_result"

        result = run_inference(data, self._model_path, self._inference_path)
        assert result == expected

    @patch("dpai.utils.uvicorn.run")
    @patch("dpai.model_manager.ModelManager")
    def test_start_app(self, mock_model_manager, mock_uvicorn_run):
        start_app(self._port, mock_model_manager.return_value)

        # Assertions
        mock_model_manager.return_value.load_models.assert_called_once()
        mock_uvicorn_run.assert_called_once_with(
            "fastapi_main:app", port=self._port, reload=True
        )
