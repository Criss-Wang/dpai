from time import time
import json

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

from application.services.models.data_models import (
    GenerationInput,
    GenerationOutput,
)
from rag.services.utils import get_pipeline_output_batch
from rag.app.service_model import ServiceModel

logger = get_logger(__name__)

generate_router = APIRouter(tags=["llm_services"])


@generate_router.post("/generate", response_model=GenerationOutput)
def generate(query: GenerationInput, request: Request) -> JSONResponse:
    """
    POST /generate
    FastAPI endpoint for xxx. The endpoint accepts a POST request with JSON payload containing the input text and a set of parameters for the generation process.

    Args:
        query (str): The input query text for the answer generation.
        parameters (GenerationParameters): A dictionary containing the parameters for the answer generation.

    Returns:
        dict: A dictionary with the following keys:
            - response (str): The answer to the user query.
            - references (list): A list of strings with reference URLs
    """

    logger.info("Running REST endpoint: generate")
    model: ServiceModel = request.app.state.model

    start_time = time()
    config = Object()

    # config.decision_engine_policy = DecisionEnginePolicies.RAG

    try:
        generation_stream = model.predict(query, config)

    except Exception as e:
        raise HTTPException(
            status_code=e.error_code_rest,
            detail=e.error_message,
        )

    try:
        pipeline_output = get_pipeline_output_batch(
            config, generation_stream, model, query, start_time
        )
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=str(e),
        )

    logger.info(f"Request summary: {json.dumps(pipeline_output.dict())}")

    return JSONResponse(content=pipeline_output.response.dict())
