import uvicorn


def main():
    from application.services.rest.factories import (
        create_rag_service_fastapi_application,
    )

    app = create_rag_service_fastapi_application()

    uvicorn.run(app, host="localhost", port=8000, timeout_keep_alive=0)


if __name__ == "__main__":
    main()
