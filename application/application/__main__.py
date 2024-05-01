import click

from application.services.cli import services
from application.utilities.logging_tools import get_logger

logger = get_logger(__name__)


@click.group()
def cli():
    pass


cli.add_command(services)


if __name__ == "__main__":
    cli()
