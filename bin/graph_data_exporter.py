#!/usr/bin/env python
"""Export components data from the graph database."""

import os

from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import __


class ComponentCorpusExporter:
    """Extract Component Names and their properties from the graph database for the SWRi Corpus

    Parameters
    ----------
    gremlin_url: str
        The URL for the gremlin remote server (i.e. the JanusGraph server websocket address)
    """

    def __init__(self, gremlin_url, logger):
        self.gremlin_url = gremlin_url
        self.g = None
        self.connection = None
        self.logger = logger

    def get_components(self):
        """Return a json serializable dictionary of properties for different components in the database"""
        component_vertices = (
            self.g.V().hasLabel("[avm]Component").values("[]Name").toList()
        )
        all_components = {}
        components_with_missing_classes = []
        self.logger.info(f"Found {len(component_vertices)} components in the database")
        for component in component_vertices:
            # In favor of correctness and timing consideration, I have chosen the following queries
            # These queries might not be the most optimal/fastest
            component_properties = self._get_fixed_properties(component)

            all_components[component] = {}

            component_class = (
                self.g.V()
                .hasLabel("[avm]Component")
                .has("[]Name", component)
                .in_()
                .hasLabel("[]Classifications")
                .in_()
                .as_("class")
                .select("class")
                .by("value")
                .toList()
            )

            self.logger.info(
                f"Extracted fixed properties for {component}. The component type is {component_class}"
            )

            for component_property in component_properties:
                all_components[component][
                    component_property["propname"]
                ] = component_property["sval"]

            all_components[component]["Classification"] = (
                component_class[0] if len(component_class) else None
            )

            if not len(component_class):
                self.logger.warning(f"Missing component classification for {component}")
                components_with_missing_classes.append(component)

            parametric_properties = self._get_parametric_properties(component)

            self.logger.info(
                f"Extracted parametric properties for {component}. Found {len(parametric_properties)}"
            )
            for component_property in parametric_properties:
                all_components[component][
                    f"para_{component_property['propname']}_{component_property['label']}"
                ] = component_property["sval"]

        return all_components, components_with_missing_classes

    def _get_fixed_properties(self, component):
        return (
            self.g.V()
            .has("[]Name", component)
            .as_("comp")
            .in_("inside")
            .hasLabel("[]Property")
            .as_("prop")
            .in_("inside")
            .in_("inside")
            .has("[http://www.w3.org/2001/XMLSchema-instance]type", "[avm]FixedValue")
            .in_("inside")
            .in_("inside")
            .as_("val")
            .select("prop")
            .by("[]Name")
            .as_("propname")
            .select("val")
            .by(__.coalesce(__.values("value"), __.constant("none")))
            .as_("sval")
            .select("propname", "sval")
            .toList()
        )

    def _get_parametric_properties(self, component):
        return (
            self.g.V()
            .has("[]Name", component)
            .as_("comp")
            .in_("inside")
            .hasLabel("[]Property")
            .as_("prop")
            .in_("inside")
            .in_("inside")
            .has(
                "[http://www.w3.org/2001/XMLSchema-instance]type",
                "[avm]ParametricValue",
            )
            .in_("inside")
            .as_("type")
            .in_("inside")
            .in_("inside")
            .as_("val")
            .select("type")
            .by(__.label())
            .as_("label")
            .select("prop")
            .by("[]Name")
            .as_("propname")
            .select("val")
            .by(__.coalesce(__.values("value"), __.constant("none")))
            .as_("sval")
            .select("propname", "sval", "label")
            .toList()
        )

    def __enter__(self):
        if not self.connection:
            self.connect()
        return self

    def __exit__(self, *args):
        return self.close()

    def close(self):
        self.connection.close()
        self.connection = None
        self.g = None
        self.logger.info("Closed connection to the gremlin server")

    def connect(self):
        self.connection = DriverRemoteConnection(self.gremlin_url, "g")
        self.g = traversal().withRemote(self.connection)
        self.logger.info(f"Connected to gremlin server at {self.gremlin_url}")


if __name__ == "__main__":
    import json
    from argparse import ArgumentParser
    from pathlib import Path

    from symbench_athens_client.utils import get_data_file_path, get_logger

    GREMLIN_URL = "ws://localhost:8182/gremlin"
    OUT_LOC = get_data_file_path(".")

    parser = ArgumentParser(
        description="The UAV Components Corpus exporter. "
        "Use this script with caution, as it "
        "can mess up your package directories."
    )
    parser.add_argument(
        "-s", "--server-url", default=GREMLIN_URL, type=str, help="The gremlin URL"
    )
    parser.add_argument(
        "-o",
        "--output",
        default=OUT_LOC,
        type=str,
        help="Where to save the output files. Note: If the directory doesn't exist, it will be created",
    )

    args = parser.parse_args()

    logger = get_logger(f"{__file__}::{__name__}::{ComponentCorpusExporter.__name__}")
    with ComponentCorpusExporter(GREMLIN_URL, logger=logger) as exporter:
        components, missing = exporter.get_components()
        save_dir = Path(args.output).resolve()
        if not save_dir.exists():
            os.makedirs(save_dir, exist_ok=True)

        with open(save_dir / "all_components.json", "w") as json_file:
            json.dump(components, json_file, indent=2)

        with open(
            save_dir / "missing_components.txt", "w"
        ) as missing_classifications_file:
            missing_classifications_file.write(
                "##Note: These components are missing classes in the database:\n"
            )
            missing_classifications_file.write(",".join(missing))
