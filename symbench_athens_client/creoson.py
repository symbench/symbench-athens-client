"""Helper Module for automating CREO mass properties in python"""
import glob
import os
import time
from functools import cmp_to_key
from pathlib import Path

import creopyson

from symbench_athens_client.models.components import Battery, Component, Motor, Wing
from symbench_athens_client.utils import get_data_file_path, get_logger


class CreosonMassPropertiesDriver:
    """The driver for creoson server for athens UAV/UAM components.

    Parameters
    ----------
    creoson_ip: str, default=localhost
        The ip address of the creoson server
    creoson_port: int, default=9056
        The port number that the server is listening to
    use_desktop: bool, default=False
        If true start creo in desktop rather than java runtime,
        useful for debugging. This is only relevent when this
        class is used for starting creo from creoson.

    Attributes
    ----------
    creoson_client: creopyson.Client object
        The creopyson client object which drives creson server and thus creo

    Notes
    -----
    Inorder to use this class, first start the creoson server, which can be
    started by running `CreosonSetup.exe` and note the ip address and port
    number for the server. There are two ways to use this class

    1. Start CREO-Parametric manually and use this class.
    2. Copy contents of C:\Program Files\PTC\Creo xxx\Parametric\bin\parametric.bat
    to a file named `nitro_proe_remote.bat` and provide its path as
    `nitro_proe_remote_loc`
    """

    def __init__(
        self,
        nitro_proe_remote_loc=None,
        creoson_ip="localhost",
        creoson_port=9056,
        use_desktop=False,
    ):
        self.creoson_client = creopyson.Client(ip_adress=creoson_ip, port=creoson_port)

        self.creoson_client.connect()
        self.logger = get_logger(name=self.__class__.__name__)
        self.logger.info(
            f"Connected to Creoson server at {creoson_ip}:{creoson_port}. "
            f"SessionID: {self.creoson_client.sessionId}"
        )
        self.start_creo(nitro_proe_remote_loc, use_desktop=use_desktop)

    def start_creo(self, starter_bat, use_desktop):
        if starter_bat and not self.creoson_client.is_creo_running():
            try:
                self.creoson_client.start_creo(starter_bat, use_desktop=use_desktop)
            except:  # ToDo: Too Broad
                self.kill_creo()
            if use_desktop:
                time.sleep(20)
            else:
                time.sleep(5)

    def kill_creo(self):
        if self.creoson_client.is_creo_running():
            self.creoson_client.kill_creo()

    def is_creo_running(self):
        return self.creoson_client.is_creo_running()

    def batch_process(self, components):
        pass

    def _load_component(self, component):
        self.logger.debug(
            f"About to load component {component.name}'s .prt file  to CREO"
        )

        dirname = get_data_file_path("CAD")
        file = component.prt_file
        loaded_files = self.creoson_client.file_list()

        if file not in loaded_files:
            self.creoson_client.file_open(
                file,
                dirname=dirname,
            )

        self.logger.info(f"Successfully loaded {file} for {component.name}")
        return file

    def set_parameters(self, component):
        file = self._load_component(component)
        parameter_list = self.creoson_client.parameter_list(name="", file_=file)
        component_params = component.dict(by_alias=True)
        params_of_interest = []

        for param in parameter_list:
            if param["name"] in component_params:
                param["value"] = component_params[param["name"]]
                params_of_interest.append(param)

        for param in params_of_interest:
            self.logger.debug(
                f"Setting {param['name']} for {component.name} to {param['value']}"
            )
            self.creoson_client.parameter_set(
                name=param["name"],
                value=param["value"],
                file_=file,
                type_=param["type"],
                no_create=True,
            )
        self.logger.info(f"Successfully set parameters for {component.name}")

    def get_parameters(self, component):
        assert isinstance(component, Component)
        file = self._load_component(component)
        return self.creoson_client.parameter_list(name="", file_=file)

    def mass_properties(self, component):
        assert isinstance(component, Component)
        self.logger.info(f"Calculating mass properties for {component.name}")

        file = self._load_component(component)
        self.set_parameters(component)

        mass_props = self.creoson_client.file_massprops(file)
        self.logger.info(
            f"Successfully calculated mass properties for {component.name}"
        )
        return mass_props
