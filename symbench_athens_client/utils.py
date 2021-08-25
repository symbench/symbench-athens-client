import logging
from functools import lru_cache
from typing import Iterable

from uav_analysis.mass_properties import hplane_fixed_bemp, quad_copter_fixed_bemp2
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
def estimate_mass_formulae(tb_data_loc, design_type="QuadCopter"):
    """Estimate mass properties of a design based on a fixed BEMP config testbench"""
    tb_data = TestbenchData()
    tb_data.load(tb_data_loc)
    assert design_type in {
        "QuadCopter",
        "HPlane",
    }, "The mass estimates only work for QuadCopter and HPlane Seed Design"
    estimator = {"QuadCopter": quad_copter_fixed_bemp2, "HPlane": hplane_fixed_bemp}
    return estimator[design_type](tb_data)


def get_mass_estimates_for(testbench_data_path, design):
    """Given a quadcopter/hplane seed design, calculate the mass properties using creo surrogate estimator.

    Parameters
    ----------
    testbench_data_path: str, pathlib.Path
        The zip file location for the uav_analusis.testbench_data.TestBenchData
    design: instance of symbench_athens_client.models.design.QuadCopter or symbench_athens_client.models.design.HPlane
        The instance of the QuadCopter seed design to estimate properties for=

    Returns
    -------
    dict
        The dictionary of mass properties estimates
    """
    from symbench_athens_client.models.designs import HPlane, QuadCopter

    assert isinstance(
        design, (QuadCopter, HPlane)
    ), "The function estimator only works for quadcopter and hplane seed design"

    aircraft_parameters = design.dict(by_alias=True, include=design.__design_vars__)
    formulae = estimate_mass_formulae(testbench_data_path, design.__class__.__name__)

    mass_properties = {}
    for key, value in formulae.items():
        mass_estimates_key = key.replace("aircraft.", "")
        try:
            mass_properties[mass_estimates_key] = value.evalf(subs=aircraft_parameters)
        except AttributeError:
            mass_properties[mass_estimates_key] = value

    return mass_properties
