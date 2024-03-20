import importlib.util as util
from typing import Any
from joblib import load

import uvicorn
from .model_manager import ModelManager, InferenceException


def run_inference(data: Any, model_path: str, inference_path: str) -> Any:
    """
    TODO: cannot load model every time, must either cache it or store it in local
    """
    spec = util.spec_from_file_location("inference", inference_path)
    assert spec is not None
    assert spec.loader is not None
    inference_file = util.module_from_spec(spec)
    spec.loader.exec_module(inference_file)

    model = load(model_path)["model"]
    try:
        inputs = inference_file.input_fn(data)
    except Exception as e:
        raise InferenceException("Failed to load data, causes:", e)

    try:
        outputs = inference_file.predict_fn(inputs, model)
        return outputs
    except Exception as e:
        raise InferenceException("Failed to run inference, causes:", e)


def start_app(port: int, model_manager: ModelManager) -> None:
    """Start the application"""
    # [TODO] save models / models' metadata to cache
    model_manager.load_models()
    uvicorn.run("fastapi_main:app", port=port, reload=True)
