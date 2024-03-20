import argparse
import os

from .utils import start_app
from .model_manager import ModelManager

# from setups import logger


def main():
    parser = argparse.ArgumentParser("dpai parser")
    subparser = parser.add_subparsers(dest="func")

    parser_register = subparser.add_parser("register", help="Register model")
    parser_register.add_argument("-n", "--name", type=str, required=True)
    parser_register.add_argument(
        "-m", "--model_path", required=True, type=os.path.abspath
    )
    parser_register.add_argument(
        "-i", "--inference_path", required=True, type=os.path.abspath
    )

    parser_serve = subparser.add_parser("serve", help="Serve model")
    parser_serve.add_argument("--port", type=int, default=9000)
    args = parser.parse_args()

    model_manager = ModelManager()

    if args.func == "register":
        # logger.info("Register")
        model_manager.register_model(args.name, args.model_path, args.inference_path)
        model_manager.load_models()

    elif args.func == "serve":
        # logger.info("serve")
        start_app(args.port, model_manager)
    else:
        raise NotImplementedError
