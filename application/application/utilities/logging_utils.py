import logging
import time
import yaml
from functools import wraps
from logging import config as logging_config


def initialize_logging(config_path):
    """
    TODO: add context var/session following the pattern from aisera neural-search project
    """
    with open(config_path) as yaml_fh:
        config_description = yaml.safe_load(yaml_fh)
        logging_config.dictConfig(config_description)

    for logger_name in [
        "elasticsearch",
        "botocore",
        "azure",
        "tools",
        "s3transfer",
        "boto3",
        "urllib3",
        "opensearch",
    ]:
        logging.getLogger(logger_name).setLevel(logging.WARNING)


def log_function_call(*args, **kwargs):
    """
    A decorator to log the name of the function, its execution time, and any exceptions raised.
    """
    reraise = kwargs.pop("reraise", True)
    return_elapsed_time = kwargs.pop("return_elapsed_time", False)

    if args and callable(args[0]):  # No arguments were passed

        @wraps(args[0])
        def wrapper(*inner_args, **inner_kwargs):
            return _log_function_execution(
                args[0], reraise, return_elapsed_time, *inner_args, **inner_kwargs
            )

        return wrapper
    else:

        def decorator(func):
            @wraps(func)
            def wrapper(*inner_args, **inner_kwargs):
                return _log_function_execution(
                    func, reraise, return_elapsed_time, *inner_args, **inner_kwargs
                )

            return wrapper

        return decorator


def _log_function_execution(func, reraise, return_time, *args, **kwargs):
    start_time = time.time()

    try:
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        logging.info(f"Function {func.__qualname__} executed in {duration:.2f} seconds")
        if return_time:
            return result, {func.__qualname__: duration}
        return result
    except Exception as e:
        logging.error(f"Function {func.__qualname__} raised an exception: {repr(e)}")
        if reraise:
            raise e  # re-raise the original exception


def measure_coroutine_time(return_elapsed_time=False):
    def decorator(coroutine_func):
        @wraps(coroutine_func)
        async def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = await coroutine_func(
                *args, **kwargs
            )  # Await the result of the coroutine
            end_time = time.perf_counter()
            duration = end_time - start_time
            logging.info(
                f"Coroutine {coroutine_func.__qualname__} took {duration:.2f} seconds"
            )
            if return_elapsed_time:
                return result, (coroutine_func.__qualname__, duration)
            return result

        return wrapper

    return decorator
