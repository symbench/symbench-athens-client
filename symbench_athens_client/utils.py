import logging
import os
import zipfile
from functools import lru_cache
from pathlib import Path
from typing import Iterable

from uav_analysis.mass_properties import quad_copter_fixed_bemp2
from uav_analysis.testbench_data import TestbenchData

from symbench_athens_client.exceptions import PropellerAssignmentError


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
def estimate_mass_formulae(tb_data_locs, estimator=quad_copter_fixed_bemp2):
    """Estimate mass properties of a design based on a fixed BEMP config testbench"""
    if estimator is None:
        estimator = quad_copter_fixed_bemp2
    tb_data_loc = list(tb_data_locs)

    tb_data = TestbenchData()
    if not isinstance(tb_data_loc, (list, set, tuple)):
        tb_data_loc = [tb_data_loc]

    tb_data_loc = [str(Path(data_loc).resolve()) for data_loc in tb_data_loc]

    for data_path in tb_data_loc:
        tb_data.load(data_path)

    return estimator(tb_data)


def get_mass_estimates_for_quadcopter(testbench_path_or_formulae, quad_copter):
    """Given a quadcopter seed design, calculate the mass properties using creo surrogate estimator.

    Parameters
    ----------
    testbench_path_or_formulae: str, pathlib.Path
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

    # ToDo: Better Way to Handle this
    aircraft_parameters.update(
        {
            "Battery_0_Weight": quad_copter.battery_0.weight,
            "Battery_0_Length": quad_copter.battery_0.length,
            "Battery_0_Width": quad_copter.battery_0.width,
            "Battery_0_Thickness": quad_copter.battery_0.thickness,
            "Prop_0_Weight": quad_copter.propeller_0.weight,
            "Prop_0_Diameter": quad_copter.propeller_0.diameter,
            "Prop_0_Thickness": quad_copter.propeller_0.hub_thickness,
        }
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


def relative_path(src, destination):
    """Given a source and destination path, find the relative path"""
    return os.path.relpath(destination, src)


def assign_propellers_quadcopter(quad_design, propeller):
    """Given a quadcopter, properly assign propellers to it such that it can rise and hover"""
    from symbench_athens_client.models.components import Propeller, Propellers
    from symbench_athens_client.models.designs import QuadCopter

    if not isinstance(quad_design, QuadCopter):
        raise TypeError("Currently, this function only supports QuadCopter design")

    if not isinstance(propeller, (Propeller, str)):
        raise TypeError(
            f"Expected {propeller} to be a Propeller instance or a string of the propeller name. "
            f"Got {type(propeller).__class__.__name__} instead"
        )

    if isinstance(propeller, str):
        propeller = Propellers[propeller]

    propellers = list(
        filter(lambda p: p.performance_file == propeller.performance_file, Propellers)
    )
    prop_0, prop_1, prop_2, prop_3 = (None,) * 4

    if propeller.direction == -1:
        prop_0 = propeller
        prop_2 = propeller
        for prop in propellers:
            if prop.direction == -1 * propeller.direction:
                prop_1 = prop
                prop_3 = prop
    else:
        prop_1 = propeller
        prop_3 = propeller
        for prop in propellers:
            if prop.direction == -1 * propeller.direction:
                prop_0 = prop
                prop_2 = prop

    if not all(isinstance(p, Propeller) for p in [prop_0, prop_1, prop_2, prop_3]):
        raise PropellerAssignmentError(
            "Error in assigning Propeller to the quadcopter design. "
            "Exact same propeller with opposite spin than provided propeller "
            "doesn't not exist in the database."
        )

    quad_design.propeller_0 = prop_0
    quad_design.propeller_1 = prop_1
    quad_design.propeller_2 = prop_2
    quad_design.propeller_3 = prop_3

    quad_design.validate_propellers_directions()
