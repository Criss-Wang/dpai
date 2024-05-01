import click


@click.group()
def services():
    pass


@services.command()
@click.option("--host", default="0.0.0.0", type=str, show_default=True)
@click.option(
    "--port", default="8000", type=click.IntRange(0, 65536), show_default=True
)
def run_rest(host, port):
    import uvicorn
    from application.services.rest.factories import (
        create_app_service_fastapi_application,
    )

    app = create_app_service_fastapi_application()
    uvicorn.run(app, host=host, port=port, timeout_keep_alive=0)
