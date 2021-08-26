import logging
import zipfile
from functools import lru_cache
from pathlib import Path
from typing import Iterable

from uav_analysis.mass_properties import quad_copter_fixed_bemp2
from uav_analysis.testbench_data import TestbenchData


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


@lru_cache(maxsize=128)
def estimate_mass_formulae(tb_data_loc):
    """Estimate mass properties of a design based on a fixed BEMP config testbench"""
    tb_data = TestbenchData()
    tb_data.load(tb_data_loc)
    return quad_copter_fixed_bemp2(tb_data)


def get_mass_estimates_for_quadcopter(testbench_path_or_formulae, quad_copter):
    """Given a quadcopter seed design, calculate the mass properties using creo surrogate estimator.

    Parameters
    ----------
    testbench_data_path: str, pathlib.Path
        The zip file location for the uav_analusis.testbench_data.TestBenchData
    quad_copter: instance of symbench_athens_client.models.design.QuadCopter
        The instance of the QuadCopter seed design to estimate properties for=

    Returns
    -------
    dict
        The dictionary of mass properties estimates
    """
    from symbench_athens_client.models.designs import QuadCopter

    assert isinstance(
        quad_copter, QuadCopter
    ), "The function estimator only works for quadcopter seed design"

    aircraft_parameters = quad_copter.dict(
        by_alias=True, include=quad_copter.__design_vars__
    )

    if isinstance(testbench_path_or_formulae, (str, Path)):
        formulae = estimate_mass_formulae(testbench_path_or_formulae)
    else:
        formulae = testbench_path_or_formulae

    mass_properties = {}
    for key, value in formulae.items():
        mass_estimates_key = key.replace("aircraft.", "")
        try:
            mass_properties[mass_estimates_key] = value.evalf(subs=aircraft_parameters)
        except AttributeError:
            mass_properties[mass_estimates_key] = value

    return mass_properties


def extract_from_zip(zip_path, output_dir, files):
    if not isinstance(zip_path, Path):
        zip_path = Path(zip_path).resolve()

    assert zip_path.exists(), "The provided path doesn't exist"
    assert zipfile.is_zipfile(zip_path), "The provided file is not a zip file"

    with zip_path.open("rb") as zip_path_bin:
        with zipfile.ZipFile(zip_path_bin) as zip_file:
            for file in zip_file.namelist():
                if file in files:
                    zip_file.extract(file, output_dir)
