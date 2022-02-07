#! /usr/bin env python
import csv

from symbench_athens_client.creoson import CreosonMassPropertiesDriver
from symbench_athens_client.models.components import (
    Batteries,
    ESCs,
    Motors,
    Propellers,
    Wings,
)


class MassPropertiesExporter:
    """Export mass-properties for all components"""

    def __init__(self, outdir, ip="localhost", port=9056):
        self.driver = CreosonMassPropertiesDriver(creoson_ip=ip, creoson_port=port)
        self.outdir = outdir

    def run(self):
        """Run the exporter for components"""
        motors = self._extract_components(Motors)
        batteries = self._extract_components(Batteries)
        propellers = self._extract_components(Propellers)
        wings = self._extract_components(Wings)
        escs = self._extract_components(ESCs)

        for name, components in zip(
            ["motors", "batteries", "propellers", "wings", "escs"],
            [motors, batteries, propellers, wings, escs],
        ):
            with open(f"{self.outdir}/{name}.csv", "w", newline="") as csvfile:
                fieldnames = components[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(components)

    def _extract_components(self, components):
        components_properties = []

        for component in components:
            component_properties = component.dict(by_alias=True)
            mass_properties = self.driver.mass_properties(component)
            component_properties.update(self._mass_props_to_csv_dict(mass_properties))
            component_properties.update(self._get_creo_parameters(component))
            components_properties.append(component_properties)

        return components_properties

    def _get_creo_parameters(self, component):
        params = self.driver.get_parameters(component)
        return {f"CREO_{param['name']}": param["value"] for param in params}

    @staticmethod
    def _mass_props_to_csv_dict(mass_props):
        """Return a csv style dict style dict"""
        return {
            "surface_area": mass_props["surface_area"],
            "density": mass_props["density"],
            # Coordinate System
            "coordIxx": mass_props["coord_sys_inertia_tensor"]["x_axis"]["x"],
            "coordIxy": mass_props["coord_sys_inertia_tensor"]["x_axis"]["y"],
            "coordIxz": mass_props["coord_sys_inertia_tensor"]["x_axis"]["z"],
            "coordIyx": mass_props["coord_sys_inertia_tensor"]["y_axis"]["x"],
            "coordIyy": mass_props["coord_sys_inertia_tensor"]["y_axis"]["y"],
            "coordIyz": mass_props["coord_sys_inertia_tensor"]["y_axis"]["z"],
            "coordIzx": mass_props["coord_sys_inertia_tensor"]["z_axis"]["x"],
            "coordIzy": mass_props["coord_sys_inertia_tensor"]["z_axis"]["y"],
            "coordIzz": mass_props["coord_sys_inertia_tensor"]["z_axis"]["z"],
            # Center of Gravity
            "cgIxx": mass_props["ctr_grav_inertia_tensor"]["x_axis"]["x"],
            "cgIxy": mass_props["ctr_grav_inertia_tensor"]["x_axis"]["y"],
            "cgIxz": mass_props["ctr_grav_inertia_tensor"]["x_axis"]["z"],
            "cgIyx": mass_props["ctr_grav_inertia_tensor"]["y_axis"]["x"],
            "cgIyy": mass_props["ctr_grav_inertia_tensor"]["y_axis"]["y"],
            "cgIyz": mass_props["ctr_grav_inertia_tensor"]["y_axis"]["z"],
            "cgIzx": mass_props["ctr_grav_inertia_tensor"]["z_axis"]["x"],
            "cgIzy": mass_props["ctr_grav_inertia_tensor"]["z_axis"]["y"],
            "cgIzz": mass_props["ctr_grav_inertia_tensor"]["z_axis"]["z"],
        }


if __name__ == "__main__":
    from argparse import ArgumentParser

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

    args = parser.parse_args()
    exporter = MassPropertiesExporter(args.outdir, args.ip_address, args.port)
    exporter.run()
