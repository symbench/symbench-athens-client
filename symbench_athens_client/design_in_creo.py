import json
import logging
from collections import defaultdict
from pathlib import Path

from creopyson import Client

from symbench_athens_client.creo_interference_client import (
    SymbenchCreoInterferenceClient,
)
from symbench_athens_client.exceptions import ParameterMismatchError
from symbench_athens_client.models.design_state_creo import (
    CreoDesignState,
    DesignInputParameter,
    Interference,
    MassProperties,
)
from symbench_athens_client.utils import get_logger


class CONSTANTS:
    ML_CYPHY_NAME = "ML_CYPHY_NAME"
    DESIGN_PARAM = "DESIGN_PARAM"
    COMPONENT_PARAM = "COMPONENT_PARAM"
    COMPONENT_NAME = "COMPONENT_NAME"
    PRT_FILE = "PRT_FILE"


class SymbenchDesingInCREO:
    """Sweep a design with multiple parameters in CREO.

    Notes
    -----
    It is assumed that CREO is open and running for this class to work.

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

    """

    def __init__(
        self,
        parameters_map,
        assembly_path,
        creoson_ip="localhost",
        creoson_port=9056,
        interference_ip="localhost",
        interference_port=8000,
    ):
        self.logger = get_logger(self.__class__.__name__, logging.DEBUG)
        self.logger.setLevel(logging.ERROR)
        self._initialize_clients(
            creoson_ip, creoson_port, interference_ip, interference_port
        )
        self._open_assembly(assembly_path)

        self.design_params = self._design_parameters_to_cad(parameters_map)

    def _initialize_clients(
        self, creoson_ip, creoson_port, interference_ip, interference_port
    ):
        """Initialize the interference and creoson clients."""
        self.creoson_client = Client(ip_adress=creoson_ip, port=creoson_port)

        self.interference_client = SymbenchCreoInterferenceClient(
            ip_address=interference_ip, port=interference_port
        )

        self.creoson_client.connect()
        self.logger.info("Successfully initialized CREOSON/Interference Clients")

    def _open_assembly(self, assembly_path):
        """Given an assembly path, open it in CREO"""
        file_path = Path(assembly_path).resolve()
        assembly_dir = str(file_path.parent)
        assembly_name = file_path.name
        self.creoson_client.file_open(
            file_=assembly_name,
            dirname=assembly_dir,
        )
        self.assembly_name = assembly_name
        self.logger.info(f"Successfully loaded the file at {assembly_path} into CREO")

    def _design_parameters_to_cad(self, parameters_map):
        """Given `parameters_map`, return mapping with CAD assembly prt info."""
        ml_cyphy_to_prt = self._ml_cyphy_to_prt()
        return self._get_design_parameters_with_cad_info(
            parameters_map, ml_cyphy_to_prt
        )

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
        return self.interference_client.get_global_interferences()

    def get_state(self, regenerate=False, flat=True):
        """Get the current state of the design from CREO.

        This method computes the mass properties and get the design parameter values and returns a json
        serializable dictionary of the design state with values.

        Parameters
        ----------
        regenerate: bool, default=False
            If True, force creo to regenerate the design

        flat: bool, default=True
            If True, return a flat csv style dictionary instead of nested dictionary
        """
        if regenerate:
            self.creoson_client.file_regenerate(file_=self.assembly_name)
        intf_data = self.get_interferences()
        interferences = None
        if intf_data["num_interferences"] > 0:
            interferences = Interference.from_dicts(intf_data["interferences"])

        mass_properties_dict = self.creoson_client.file_massprops(
            file_=self.assembly_name
        )

        mass_props = MassProperties.from_creoson_dict(mass_properties_dict)
        cad_params_dict = self.get_creo_parameters()
        parameters = [
            DesignInputParameter(name=k, value=v) for k, v in cad_params_dict.items()
        ]

        design_state = CreoDesignState(
            interferences=interferences or [],
            parameters=parameters,
            mass_properties=mass_props,
        )

        return design_state.flat_dict() if flat else design_state.dict()
