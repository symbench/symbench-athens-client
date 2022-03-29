"""Process, get/set state of a design in CREO."""
import json
import logging
import os
import uuid
from collections import defaultdict
from pathlib import Path

import creopyson
from creopyson import Client

from symbench_athens_client.creo_properties_client import SymbenchCreoPropertiesClient
from symbench_athens_client.exceptions import (
    ParameterMismatchError,
    ParameterNotFoundError,
)
from symbench_athens_client.models.design_state_creo import (
    CreoDesignState,
    DesignInputParameter,
    Interference,
    MassProperties,
)
from symbench_athens_client.utils import get_logger, projected_areas


class CONSTANTS:
    ML_CYPHY_NAME = "ML_CYPHY_NAME"
    DESIGN_PARAM = "DESIGN_PARAM"
    COMPONENT_PARAM = "COMPONENT_PARAM"
    COMPONENT_NAME = "COMPONENT_NAME"
    PRT_FILE = "PRT_FILE"


class SymbenchDesignInCREO:
    """Sweep a design with multiple parameters in CREO.

    Notes
    -----
    It is assumed that CREO, CREOSON server as well as the interference server
    are open and running for this class to work.

    Parameters
    ----------
    parameters_map: dict, required
        The GME testbench ParametersMap Dictionary for the design

    assembly_path: str, pathlib.Path, required
        The assembly path for the design

    creoson_ip: str, default="localhost"
        The ip address of the CREOSON server

    creoson_port: int, default=9056
        The port for the CREOSON server

    interference_ip: str, default="localhost"
        The ip address of the CREOSON server

    creoson_port: int, default=9056
        The port for the CREOSON server

    debug: bool, default=False
        If True, printout verbose logs
    """

    def __init__(
        self,
        parameters_map,
        assembly_path,
        creoson_ip="localhost",
        creoson_port=9056,
        interference_ip="localhost",
        interference_port=8000,
        debug=False,
    ):
        self.logger = get_logger(self.__class__.__name__, logging.DEBUG)
        self.logger.setLevel(logging.DEBUG if debug else logging.INFO)

        self._initialize_clients(
            creoson_ip, creoson_port, interference_ip, interference_port
        )

        self.assembly_name = self._open_assembly(assembly_path)

        self._bookkeep_design_params(parameters_map)

    def _initialize_clients(
        self, creoson_ip, creoson_port, interference_ip, interference_port
    ):
        """Initialize the interference and creoson clients."""
        self.creoson_client = Client(ip_adress=creoson_ip, port=creoson_port)

        self.creo_properties_client = SymbenchCreoPropertiesClient(
            ip_address=interference_ip, port=interference_port
        )

        self.creoson_client.connect()
        self.logger.info("Successfully initialized CREOSON and CreoProperties Clients")

    def _open_assembly(self, assembly_path):
        """Given an assembly path, open it in CREO"""
        file_path = Path(assembly_path).resolve()
        assembly_dir = str(file_path.parent)
        assembly_name = file_path.name
        self.creoson_client.file_open(
            file_=assembly_name,
            dirname=assembly_dir,
        )
        return assembly_name

    def _bookkeep_design_params(self, parameters_map):
        """Given `parameters_map`, return mapping with CAD assembly prt info."""
        ml_cyphy_to_prt = self._ml_cyphy_to_prt()
        self.prt_to_ml_cyphy = {v: k for k, v in ml_cyphy_to_prt.items()}

        self.design_params = self._get_design_parameters_with_cad_info(
            parameters_map, ml_cyphy_to_prt
        )
        # with open("./TrowelCADData/ConsolidatedParametersMap.json", 'w') as \
        #         json_file:
        #     json.dump(self.design_params, json_file, indent=2)
        self.logger.info("Initialized design parameter and component to GME name map")

    def _get_design_parameters_with_cad_info(self, params, ml_cyphy_to_prt):
        """Add cad .prt info and map design to cad params."""
        design_params = defaultdict(list)
        for param in params:
            ml_cyphy_name = param[CONSTANTS.COMPONENT_NAME]
            prt_file = ml_cyphy_to_prt[ml_cyphy_name]
            param[CONSTANTS.PRT_FILE] = prt_file
            design_params[param[CONSTANTS.DESIGN_PARAM]].append(param)
            self.logger.debug(
                f"Parameter `{param[CONSTANTS.DESIGN_PARAM]}` controls "
                f"parameter `{param[CONSTANTS.COMPONENT_PARAM]}` of component "
                f"{ml_cyphy_name}. The part file for it is {prt_file}."
            )

        return design_params

    def _ml_cyphy_to_prt(self):
        """Returns a mapping between component and its corresponding .prt file in GME."""
        all_prt_files = filter(
            lambda f: f.endswith(".prt"), self.creoson_client.file_list(file_="*")
        )
        ml_cyphy_to_prt = {}
        for file in all_prt_files:
            ml_cyphy_name = self.ml_cyphy_name(file)
            if ml_cyphy_name:
                self.logger.debug(f"{file} is mapped from {ml_cyphy_name} in GME")
                ml_cyphy_to_prt[ml_cyphy_name] = file

        return ml_cyphy_to_prt

    def ml_cyphy_name(self, prt_file):
        """Return the GME name for the `prt_file`."""
        ml_cyphy_param = self.creoson_client.parameter_list(
            name=CONSTANTS.ML_CYPHY_NAME, file_=prt_file
        )
        if ml_cyphy_param:
            ml_cyphy_param = ml_cyphy_param.pop()
            return ml_cyphy_param["value"]

    def _get_creo_values(self, param_details):
        """Get CREO values for a parameter"""
        all_values = []
        for detail in param_details:
            param = self.creoson_client.parameter_list(
                detail[CONSTANTS.COMPONENT_PARAM], file_=detail[CONSTANTS.PRT_FILE]
            )
            if param:
                all_values.append(param[0]["value"])
        return all_values

    def get_creo_parameters(self):
        """Get a dictionary of parameters and their values for the design"""
        cad_params = {}
        for param in self.design_params:
            values = self._get_creo_values(self.design_params[param])
            if values and len(set(values)) == 1:
                cad_params[param] = values[0]
            elif len(set(values)) > 1:
                raise ParameterMismatchError(
                    f"Multiple Values found for parameter {param}: {values}"
                )
            else:
                self.logger.debug(f"No CREO parameter found. Skipping {param}")
        return cad_params

    def get_interferences(self):
        return self.creo_properties_client.get_global_interferences()

    def _propagate_parameter(self, parameter, value):
        """Propagate a design parameter to CREO"""
        if parameter not in self.design_params:
            raise ParameterNotFoundError(
                f"Parameter {parameter} is not one of the design parameters"
            )

        param_details = self.design_params[parameter]

        for param in param_details:
            creo_param_name = param[CONSTANTS.COMPONENT_PARAM]
            creo_prt_file = param[CONSTANTS.PRT_FILE]

            creo_param = self.creoson_client.parameter_list(
                name=creo_param_name, file_=creo_prt_file
            ).pop()

            self.creoson_client.parameter_set(
                name=creo_param["name"],
                value=value,
                file_=creo_prt_file,
                type_=creo_param["type"],
                no_create=True,
            )
            self.logger.info(
                f"Set {parameter} for {param[CONSTANTS.COMPONENT_NAME]} "
                f"in CREO ( {creo_prt_file}'s {creo_param_name} = {value} )"
            )

    def _regenerate_assembly(self):
        """Regenerate the currently loaded assembly in CREO."""
        self.creoson_client.file_regenerate(file_=self.assembly_name)

    def _export_stl(self, save_path, guid):
        save_path = Path(save_path or self.creoson_client.creo_pwd()).resolve()
        filename = guid[0:31] + ".stl"
        response = self.creoson_client.interface_export_file(
            file_type="STL", filename=filename, dirname=str(save_path)
        )

        stl_loc = response["dirname"] + os.sep + response["filename"]
        self.logger.info(f"Saving stl for the current design state {stl_loc}")
        return stl_loc

    def _get_projected_areas(self, stl_loc):
        """Get the projected areas for the currently loaded design in CREO.

        Notes
        -----
        If save path is provided, the stl file will be saved in that location
        """

        areas = projected_areas(stl_loc)
        self.logger.info(f"Calculated projected areas {areas}")
        return areas

    def _swap_intf_prts_with_cyphy_names(self, intf_data):
        for data in intf_data:
            data["part_1_name"] = self.prt_to_ml_cyphy[
                data["part_1_name"].lower() + ".prt"
            ]
            data["part_2_name"] = self.prt_to_ml_cyphy[
                data["part_2_name"].lower() + ".prt"
            ]

    def get_state(self, guid=None, stl_path=None):
        """Get the current state of the design from CREO.

        This method computes the mass properties and get the design parameter values and returns a json
        serializable dictionary of the design state with values.

        Parameters
        ----------
        stl_path: str, pathlib.Path
            The path of the STL File, for projected-area calculations

        guid: str
            The guid to set for this state

        Returns
        -------
        CreoDesignState
            The state of the design in CREO

        See Also
        --------
        symbench_athens_client.models.design_state_creo.CreoDesignState
            This class encapsulates mass properties, input parameters as well as
            the interferences in the creo design at the point.
        """
        stl_loc = stl_path

        if not guid:
            self._regenerate_assembly()
            guid = str(uuid.uuid4())
            stl_loc = self._export_stl(
                Path(stl_path or self.creoson_client.creo_pwd()).resolve(), guid
            )

        intf_data = self.get_interferences()
        interferences = None
        if intf_data["num_interferences"] > 0:
            self._swap_intf_prts_with_cyphy_names(intf_data["interferences"])
            interferences = Interference.from_dicts(intf_data["interferences"])

        mass_properties_dict = self.creo_properties_client.get_massproperties()

        mass_props = MassProperties.from_creoson_dict(mass_properties_dict)
        cad_params_dict = self.get_creo_parameters()
        parameters = [
            DesignInputParameter(name=k, value=v) for k, v in cad_params_dict.items()
        ]

        design_state = CreoDesignState(
            interferences=interferences or [],
            parameters=parameters,
            mass_properties=mass_props,
            projected_areas=self._get_projected_areas(stl_loc),
        )

        if not stl_path:
            os.remove(stl_loc)

        return design_state

    def apply_params(self, params, stl_path=None):
        """Apply the parameters from a dictionary regenerate the design in CREO, and return the design state"""
        for key, value in params.items():
            self._propagate_parameter(key, value)

        self.logger.debug("Propagated parameters, regenerating assembly")
        self._regenerate_assembly()
        self.logger.info(
            "Successfully regenerated assembly after propagating parameters"
        )
        regenerated_uuid = str(uuid.uuid4())

        stl_loc = self._export_stl(stl_path, regenerated_uuid)

        state = self.get_state(regenerated_uuid, stl_path=stl_loc)

        if not stl_path:
            os.remove(stl_loc)

        return state
