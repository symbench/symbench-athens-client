#!/usr/bin/env python
"""Generate CSV files (one per component type) from the database"""
import os
import pathlib

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

    parser = argparse.ArgumentParser("The CSV Exporter for components")
    parser.add_argument(
        "-c",
        "--corpus",
        choices={"uav", "uam"},
        default="uav",
        descrption="The corpus to export",
        type=str,
    )

    parser.add_argument(
        "-d",
        "--save-dir",
        default=".",
        descrption="The directory to save the csv files in",
        type=str,
    )

    args = parser.parse_args()

    save_dir = pathlib.Path(args.save_dir).resolve()

    if not save_dir.exists():
        os.makedirs(save_dir, exist_ok=True)

    if not save_dir.is_dir():
        raise NotADirectoryError(f"{save_dir} is not a directory")

    for cls in Battery, Motor, Propeller, Wing:
        builder = ComponentsRepository(
            cls, get_all_components_of_class(Battery, corpus=args.corpus)
        )
        builder.to_csv(f"{cls.__name__}.csv")
