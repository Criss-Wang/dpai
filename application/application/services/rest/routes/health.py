from fastapi import APIRouter, Request
from starlette.responses import JSONResponse

from application import __version__
from application.services.context import launch_date

health_router = APIRouter(prefix="/health")


@health_router.get("/", tags=["health"])
def health(request: Request):
    model = (
        request.app.state.model
    )  # Access the model from the FastAPI application state
    if model.healthy():
        return {
            "status": "Active",
            "deployment_date": launch_date.get().isoformat(),
            "release": __version__,
        }
    else:
        content = {"message": "Service Unavailable"}
        return JSONResponse(content=content, status_code=503)
