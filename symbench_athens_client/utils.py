import logging
import re


def get_logger(name, level):
    """Get a logger instance."""
    logger = logging.getLogger(name)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    ch.setFormatter(formatter)

    logger.setLevel(level)
    logger.addHandler(ch)

    return logger


def to_camel_case(string):
    """Convert a string to camelcase"""
    string = "".join(string.split(" "))
    string = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", string)
    string = re.sub("__([A-Z])", r"_\1", string)
    string = re.sub(r"[-~.]", "_", string)
    string = re.sub("([a-z0-9])([A-Z])", r"\1_\2", string)
    return string.lower()


def get_data_file_path(filename):
    """Get the full path of the filename in the package's data directory"""
    from pkg_resources import resource_filename

    return resource_filename("symbench_athens_client", f"data/{filename}")
