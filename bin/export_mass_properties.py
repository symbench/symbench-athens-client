#! /usr/bin env python
import csv
import json
import time

from symbench_athens_client.creoson import CreosonMassPropertiesDriver
from symbench_athens_client.models.design_state_creo import MassProperties


class MassPropertiesExporter:
    """Export mass-properties for all components using CREOSON/creopyson.

    Attributes
    ----------
    outdir: str
        The location to save generated CSVs in
    ip: str, default=localhost
        The ip address of the CREOSON server

    See Also
    --------
    symbench_athens_client.creoson.CreosonMassPropertiesDriver
        Symbench Athens Client's driver for CREO
    """

    def __init__(self, outdir, ip="localhost", port=9056):
        self.driver = CreosonMassPropertiesDriver(creoson_ip=ip, creoson_port=port)
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
        "--ip-address",
        "-ip",
        help="The IP address of the creoson server",
        default="localhost",
        type=str,
    )
    parser.add_argument(
        "--port",
        "-p",
        help="The port number which the creoson server is listening from",
        default=9056,
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
    exporter = MassPropertiesExporter(outdir, args.ip_address, args.port)
    exporter.run(args.corpus)
