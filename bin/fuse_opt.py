import csv
import json
import logging
import pickle
import subprocess
import time

import numpy as np
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem
from pymoo.optimize import minimize

from symbench_athens_client.design_in_creo import SymbenchDesignInCREO
from symbench_athens_client.utils import create_directory


class FuselageOptimizationProblem(ElementwiseProblem):
    def __init__(self, design_in_creo, parameters_index, xl, xu):

        self.design_in_creo = design_in_creo
        self.parameters_index = parameters_index

        super().__init__(
            n_var=len(self.parameters_index),
            n_obj=2,  # Minimize Mass, SurfaceArea
            n_constr=1,  # No Interferences
            xl=xl,
            xu=xu,
        )

    def total_intf_volume(self, interferences):
        return sum(interference.interference_volume for interference in interferences)

    def _evaluate(self, x, out, *args, **kwargs):
        params_dict = {}

        for key, values in self.parameters_index.items():
            for val in values:
                params_dict[val] = x[key]
        try:
            state = self.design_in_creo.apply_params(params_dict)
        except ConnectionError:
            p = subprocess.Popen(["restart_creoson.bat"], shell=False)
            time.sleep(5)
            self.design_in_creo._initialize_clients(
                "localhost", 9056, "localhost", 8000
            )
            state = self.design_in_creo.apply_params(params_dict)

        out["F"] = [state.mass_properties.mass, params_dict["SphereDiameter"]]
        out["G"] = [
            self.total_intf_volume(state.interferences) if state.interferences else 0
        ]

        if not state.interferences:
            params_dict["Mass"] = state.mass_properties.mass
            params_dict["Interference"] = 0.0
            params_dict["ProjectedAreaProxy"] = params_dict["SphereDiameter"]

        print(params_dict, out["F"], out["G"])


def optimize(problem, algorithm, n_generations=100):
    result = minimize(
        problem, algorithm, ("n_gen", n_generations), verbose=True, seed=1
    )

    return result


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser("Pareto Optimal Fuselage parameters with NGSA-2")

    parser.add_argument(
        "asm", type=str, metavar="ASM", help="The location of the Fuselage assembly"
    )

    parser.add_argument(
        "parameters_map",
        type=str,
        metavar="PARAM_MAP",
        help="The JSON file of the parameter maps",
    )

    parser.add_argument(
        "--pop-size", type=int, default=100, help="The " "population size"
    )
    parser.add_argument(
        "--n-generations", type=int, default=100, help="The number of generations"
    )

    parser.add_argument(
        "--outdir",
        default="./results-fuselage-optimization",
        help="The results will be saved here",
    )

    args = parser.parse_args()

    with open(args.parameters_map, "r") as params_map_file:
        parameters = json.load(params_map_file)

    parameters_index = {
        0: ["TailDiameter"],
        1: ["Length"],
        2: ["FloorHeight"],
        3: ["MiddleLength"],
        4: ["SphereDiameter"],
        5: ["Seat1FB", "Seat2FB"],
    }

    xl = np.array([100, 1500, 130, 200, 1300, 750])
    xu = np.array([200, 2000, 150, 400, 1520, 790])

    fuse_problem = FuselageOptimizationProblem(
        design_in_creo=SymbenchDesignInCREO(
            parameters_map=parameters, assembly_path=args.asm
        ),
        parameters_index=parameters_index,
        xu=xu,
        xl=xl,
    )

    ngsa2 = NSGA2(pop_size=args.pop_size)

    out = optimize(fuse_problem, algorithm=ngsa2, n_generations=args.n_generations)

    savedir = create_directory(args.outdir)

    with open(
        savedir / f"results_{time.strftime('%b_%d_%Y_%H_%M_%S', time.localtime())}.pkl",
        "wb",
    ) as pklfile:
        pickle.dump({"X": out.X, "F": out.F}, pklfile)
