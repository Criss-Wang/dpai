import json
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Histogram, Counter, start_http_server
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.concurrency import iterate_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.types import Message

# Import your machine learning model and any necessary dependencies


async def set_body(request: Request, body: bytes):
    async def receive() -> Message:
        return {"type": "http.request", "body": body}

    request._receive = receive


async def get_body(request: Request) -> bytes:
    body = await request.body()
    await set_body(request, body)
    return body


class PrometheusCORSMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.cors_middleware = CORSMiddleware(
            app,
            allow_origins="*",
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.hist_data = Histogram(
            "hist_data",
            "data for histogram",
            buckets=[0, 1, 10, 100, 1000, 2000],
        )
        self.service_exceptions_counter = Counter(
            "service_exceptions_counter",
            "Exceptions counter",
        )
        self.service_exceptions_counter.inc(0)

    async def dispatch(self, request, call_next):
        await set_body(request, await request.body())
        generate_request = request.url.path in ["/generate", "/generate/"]
        user_input = await get_body(request)
        if generate_request:
            user_input = json.loads(user_input.decode("utf-8"))
            request_word_count = request.app.state.metrics_handler.get_word_count(
                user_input["query"]
            )

            self.hist_data.observe(request_word_count)
        try:
            response = await call_next(request)
        except Exception as e:
            self.service_exceptions_counter.inc()
            raise e

        if response.status_code == 200 and generate_request:
            response_body = [section async for section in response.body_iterator]
            response.body_iterator = iterate_in_threadpool(iter(response_body))
            res_dict = json.loads(response_body[0].decode())
            if len(res_dict.get("error", "")) > 0:
                self.service_exceptions_counter.inc()
            res_body = res_dict.get("generated_text", "")
            response_word_count = request.app.state.metrics_handler.get_word_count(
                res_body
            )

            self.hist_data.observe(response_word_count)

            return response
        if response.status_code != 200:
            self.service_exceptions_counter.inc()
        return response


def create_rag_service_fastapi_application() -> FastAPI:
    """
    Factory function to create a FastAPI application and register the project's routes
    :return: the FastAPI application
    """

    enable_docs = bool(os.environ.get("SHOW_DOCS", True))

    docs_args = {}
    if enable_docs is False:
        docs_args = {"docs_url": None, "redoc_url": None}
    start_http_server(8082)
    api = FastAPI(**docs_args)
    Instrumentator().instrument(api, metric_namespace="api_service")

    api.add_middleware(
        PrometheusCORSMiddleware,
    )
    metrics_handler = PrometheusMetrics()
    service_model = ServiceModel()
    register_routers(api)
    api.state.model = service_model  # Store the model in the FastAPI application state
    api.state.metrics_handler = (
        metrics_handler  # Store the model in the FastAPI application state
    )
    return api


def register_routers(api: FastAPI):
    """
    Registers the project's routes to the FastAPI application
    :param api: the FastAPI application on which to register the routes
    """
    from application.services.rest.routes.health import health_router
    from application.services.rest.routes.predict import generate_router

    api.include_router(health_router)
    api.include_router(generate_router)
