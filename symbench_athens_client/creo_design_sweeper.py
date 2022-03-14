import logging
from pathlib import Path

from creopyson import Client

from symbench_athens_client.creo_interference_client import (
    SymbenchCreoInterferenceClient,
)
from symbench_athens_client.utils import get_logger


class CREODesignSweeper:
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

    results_dir: str, pathlib.Path, default="."
        Where to save the output of the sweep

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
        self._initialize_clients(
            creoson_ip, creoson_port, interference_ip, interference_port
        )
        self._open_assembly(assembly_path)

        # ToDo: Map parameters to CAD Parts
        # Sample and Sweep

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
        self.logger.info(f"Successfully loaded the file at {assembly_path} into CREO")

    def sweep(self, parameter_ranges, number_of_samples=10000, sampling_method="lhs"):
        pass


if __name__ == "__main__":
    sweeper = CREODesignSweeper(
        parameters_map={}, assembly_path="./TestBench_CADTB_V1/uav_1.asm"
    )
