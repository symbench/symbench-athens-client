#! /usr/bin env python
import csv
import json
import time

from symbench_athens_client.component_massproperties import CreosonMassPropertiesDriver
from symbench_athens_client.models.design_state_creo import MassProperties


class MassPropertiesExporter:
    """Export mass-properties for all components using CREOSON/creopyson.

    Attributes
    ----------
    outdir: str
        The location to save generated CSVs in
    creoson_ip: str, default=localhost
        The ip address of the creoson server
    creoson_port: int, default=9056
        The port number that the server is listening to
    creo_properties_server_ip: str, default=localhost
        The ip address of the symbench creo properties server
    creo_properties_server_port: int, default=8000
        The port number that the symbench creo properties server is listening in

    See Also
    --------
    symbench_athens_client.creoson.CreosonMassPropertiesDriver
        Symbench Athens Client's driver for CREO
    """

    def __init__(
        self,
        outdir,
        creoson_ip="localhost",
        creoson_port=9056,
        creo_properties_server_ip="localhost",
        creo_properties_server_port=8000,
    ):
        self.driver = CreosonMassPropertiesDriver(
            creoson_ip=creoson_ip,
            creoson_port=creoson_port,
            creo_properties_server_ip=creo_properties_server_ip,
            creo_properties_server_port=creo_properties_server_port,
        )
        self.outdir = outdir

    def run(self, corpus):
        """Run the exporter for components' mass properties and save csv file of extracted properties."""
        if corpus == "uav":
            from symbench_athens_client.models.uav_components import (
                Batteries,
                ESCs,
                Motors,
                Propellers,
                Wings,
            )

            components_and_prefix = [
                (Motors, "motors"),
                (Batteries, "batteries"),
                (Propellers, "propellers"),
                (Wings, "wings"),
                (ESCs, "esc"),
            ]

        elif corpus == "uam":
            from symbench_athens_client.models.uam_components import (
                Batteries,
                Motors,
                Propellers,
            )

            components_and_prefix = [
                (Motors, "motors"),
                (Batteries, "batteries"),
                (Propellers, "propellers"),
            ]
        else:
            raise ValueError(f"Unknown corpus {corpus}")

        for (Components, prefix) in components_and_prefix:
            components, failed_components = self._extract_components(Components)
            self.write_files(prefix, components, failed_components)

    def write_files(self, prefix, data, failures):
        """Write files exports for `csv` and `json` for components mass properties."""
        self._write_csv(prefix, data)
        self._write_json("failed_" + prefix, failures)

    def _write_json(self, prefix, data):
        with open(f"{self.outdir}/{prefix}.json", "w", newline="") as json_file:
            json.dump(data, json_file)

    def _write_csv(self, prefix, data):
        with open(f"{self.outdir}/{prefix}.csv", "w", newline="") as csvfile:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    def _extract_components(self, components):
        """Extract mass properties for components."""
        components_properties = []
        failed = {}

        for component in components:
            try:
                component_properties = component.dict(by_alias=True)
                mass_properties = self.driver.mass_properties(component)
                component_properties.update(
                    MassProperties.from_creoson_dict(mass_properties).dict()
                )
                component_properties.update(self._get_creo_parameters(component))
                components_properties.append(component_properties)
                time.sleep(0.001)

            except Exception as e:
                self.driver.logger.debug(e)
                failed[component.name] = str(e)

        return components_properties, failed

    def _get_creo_parameters(self, component):
        """Get CREO parameters for a component."""
        params = self.driver.get_creo_parameters(component)
        return {f"CREO_{param['name']}": param["value"] for param in params}

    @staticmethod
    def _mass_props_to_csv_dict(mass_props):
        """Return a csv style dict from creopyson mass-properties dict."""
        return MassProperties.from_creoson_dict(mass_props).dict()


if __name__ == "__main__":
    from argparse import ArgumentParser

    from symbench_athens_client.utils import create_directory

    parser = ArgumentParser("Export mass properties for UAV Components")
    parser.add_argument(
        "outdir",
        metavar="OUTDIR",
        help="The output directory to save the exported csv files to",
        type=str,
    )
    parser.add_argument(
        "--creoson-ip",
        "-crip",
        help="The IP address of the creoson server",
        default="localhost",
        type=str,
    )
    parser.add_argument(
        "--creoson-port",
        "-crp",
        help="The port number which the creoson server is listening from",
        default=9056,
        type=int,
    )

    parser.add_argument(
        "--creo-properties-ip",
        "-cpip",
        help="The IP address of the symbench creo properties server",
        default="localhost",
        type=str,
    )
    parser.add_argument(
        "--creo-properties-server-port",
        "-cpp",
        help="The port number which the symbench creo properties server is listening from",
        default=8000,
        type=int,
    )

    parser.add_argument(
        "-c",
        "--corpus",
        help="The corpus to extract components from",
        choices={"uav", "uam"},
        default="uam",
        type=str,
    )

    args = parser.parse_args()
    outdir = create_directory(dir_name=args.outdir)
    exporter = MassPropertiesExporter(
        outdir,
        creoson_ip=args.creoson_ip,
        creoson_port=args.creoson_port,
        creo_properties_server_ip=args.creo_properties_server_ip,
        creo_properties_server_port=args.creo_properties_server_port,
    )
    exporter.run(args.corpus)
