import logging
import re


def get_logger(name, level=logging.DEBUG):
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


def get_data_file_path(filename):
    """Get the full path of the filename in the package's data directory"""
    from pkg_resources import resource_filename

    return resource_filename("symbench_athens_client", f"data/{filename}")


def inject_none_for_missing_fields(cls, values):
    """Given a BaseModel class and a dictionary to populate its fields, inject None for missing fields."""
    for field_name, field_info in cls.__fields__.items():
        if field_name not in values and field_info.alias not in values:
            values[field_name] = None
    return values


def dict_to_string(inp_dict, repeat_values=True):
    """Convert a dictionary to a comma separated string of key=value or key=value,value"""
    return "".join(
        f"{k}={v},{v} " if repeat_values else f"{k}={v} " for k, v in inp_dict.items()
    ).rstrip()
