import logging
from typing import Iterable


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


def dict_to_design_vars(inp_dict, repeat_values=True):
    """Convert a dictionary to a comma separated string to be used as jenkins pipeline input"""
    should_repeat = lambda v: repeat_values and not isinstance(v, Iterable)
    get_single = lambda v: ",".join(str(x) for x in v) if isinstance(v, Iterable) else v

    return "".join(
        f"{k}={v},{v} " if should_repeat(v) else f"{k}={get_single(v)} "
        for k, v in inp_dict.items()
    ).rstrip()
