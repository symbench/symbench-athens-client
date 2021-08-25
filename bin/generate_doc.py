#!/usr/bin/env python
"""Generate documentation for selective classes of the package."""

from tomark import Tomark

from symbench_athens_client.models.designs import (
    HCopter,
    HPlane,
    QuadCopter,
    QuadSpiderCopter,
)
from symbench_athens_client.models.uav_pipelines import (
    CircularFlight,
    FlightPathsAll,
    GeometryV1,
    HoverCalc,
    InitialConditionsFlight,
    RacingOvalFlight,
    RiseAndHoverFlight,
    StraightLineFlight,
    TrimSteadyFlight,
)


class DocsGenerator:
    @staticmethod
    def generate_for_design(seed_design_classes):
        md = ["# Seed designs"]
        for cls in seed_design_classes:
            md.append(f"\n## {cls.__name__}")
            md.append(f"\n{cls.__doc__}\n")
            md.append(f"\n Parameters are listed below:\n")
            fields = []
            for field, field_info in cls.__fields__.items():
                if field != "name" and field != "swap_list":
                    fields.append(
                        {
                            "name": field,
                            "Name in Graph": field_info.alias,
                            "default": field_info.default
                            if field in cls.__design_vars__
                            else field_info.default.name,
                        }
                    )

            md.append(Tomark.table(fields))
            md.append("\n\n### Jenkins Design Variables and Defaults:")
            md.append(Tomark.table([cls().to_jenkins_parameters()]))
            md.append("\n\n")
        return "\n".join(md)

    @staticmethod
    def generate_for_pipelines(pipeline_classes):
        md = ["# UAV Workflow Pipelines"]
        for cls in pipeline_classes:
            md.append(f"\n## {cls.__name__}")
            md.append(f"\n{cls.__doc__}\n")

            parameters = []
            fixed_parameters = []
            for field, field_info in cls.__fields__.items():
                if hasattr(cls, "__design_vars__") and field in cls.__design_vars__:
                    parameters.append(
                        {
                            "name": field,
                            "Jenkins Name": field_info.alias,
                            "default": field_info.default,
                            "description": field_info.field_info.description,
                        }
                    )
            cls_instance = cls(design=QuadCopter())
            if hasattr(cls, "__fixed_design_vars__"):
                for key, value in cls.__fixed_design_vars__.items():
                    fixed_parameters.append(
                        {
                            "name": key,
                            "Jenkins Name": value,
                            "default": getattr(cls_instance, key),
                            "description": None,
                        }
                    )
            if parameters:
                md.append(f"\n Parameters that can be changed are listed below:\n")
                md.append(Tomark.table(parameters))

            if fixed_parameters:
                md.append(f"\n Parameters that can't be changed are listed below:\n")
                md.append(Tomark.table(fixed_parameters))

            md.append(
                "\n\n### Jenkins Design Variables and Defaults (Assuming a QuadCopter seed design):"
            )
            md.append(Tomark.table([cls_instance.to_jenkins_parameters()]))
            md.append("\n\n")
        return "\n".join(md)


if __name__ == "__main__":
    from pathlib import Path

    DOCS_BASE = Path(__file__).parent.resolve() / ".." / "docs"
    designs_md = DocsGenerator.generate_for_design(
        [QuadCopter, QuadSpiderCopter, HCopter, HPlane]
    )

    pipelines_md = DocsGenerator.generate_for_pipelines(
        [
            GeometryV1,
            HoverCalc,
            TrimSteadyFlight,
            InitialConditionsFlight,
            StraightLineFlight,
            CircularFlight,
            RiseAndHoverFlight,
            RacingOvalFlight,
            FlightPathsAll,
        ]
    )

    with open(DOCS_BASE / "seed_designs.md", "w") as d_file:
        d_file.write(designs_md)

    with open(DOCS_BASE / "uav_pipelines.md", "w") as p_file:
        p_file.write(pipelines_md)
