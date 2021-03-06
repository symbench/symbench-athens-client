#!/usr/bin/env python
"""Generate CSV files (one per component type) from the database"""

from symbench_athens_client.models.component import (
    Battery,
    ComponentsRepository,
    Motor,
    Propeller,
    Wing,
    get_all_components_of_class,
)

if __name__ == "__main__":
    import argparse

    from symbench_athens_client.utils import create_directory

    parser = argparse.ArgumentParser("The CSV Exporter for components")
    parser.add_argument(
        "-c",
        "--corpus",
        choices={"uav", "uam"},
        default="uav",
        help="The corpus to export",
        type=str,
    )

    parser.add_argument(
        "-d",
        "--save-dir",
        default=".",
        help="The directory to save the csv files in",
        type=str,
    )

    args = parser.parse_args()

    save_dir = create_directory(dir_name=args.save_dir)

    for cls in Battery, Motor, Propeller, Wing:
        builder = ComponentsRepository(
            cls,
            get_all_components_of_class(cls, corpus=args.corpus),
            corpus=args.corpus,
        )
        builder.to_csv(f"{save_dir}/{args.corpus.upper()}_{cls.__name__}.csv")
