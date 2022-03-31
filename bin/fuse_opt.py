"""Multi-Objective optimization for fuselage."""
import csv
import json
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
    """The optimization problem for Fuselage, framed in CREO"""

    def __init__(self, design_in_creo, parameters_index, xl, xu):

        self.design_in_creo = design_in_creo
        self.parameters_index = parameters_index

        super().__init__(
            n_var=len(self.parameters_index),
            n_obj=2,  # Minimize Mass, SurfaceArea
            n_constr=3,  # No Interferences, SEAT_1_FB < Length, SEAT_2_FB <  Length
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
            self.total_intf_volume(state.interferences) if state.interferences else 0,
            params_dict["Seat1FB"] - params_dict["Length"],
            params_dict["Seat2FB"] - params_dict["Length"],
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


def get_pareto_csv_dict(parameters_index, X, F):
    pareto_optimal_sets = []

    for x, y in zip(X, F):
        res = {}
        for key in parameters_index:
            res[parameters_index[key][0]] = x[key]
            if len(parameters_index[key]) > 1:
                res[parameters_index[key][1]] = x[key]
        res["Mass"] = y[0]
        pareto_optimal_sets.append(res)

    return pareto_optimal_sets


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser("Fuselage Optimization")
    subparsers = parser.add_subparsers(help="help for subcommand", dest="subcommand")

    opt_cmd = subparsers.add_parser(
        "optimize", help="optimize the fuselage using NSGA algorithm"
    )

    analyze_results = subparsers.add_parser("analyze", help="Analyze the results")

    opt_cmd.add_argument(
        "asm", type=str, metavar="ASM", help="The location of the Fuselage assembly"
    )

    opt_cmd.add_argument(
        "parameters_map",
        type=str,
        metavar="PARAM_MAP",
        help="The JSON file of the parameter maps",
    )

    opt_cmd.add_argument(
        "--seats-config",
        default="side_by_side",
        choices={"side_by_side", "front_to_back"},
        type=str,
        help="The seats " "configuration",
    )

    opt_cmd.add_argument(
        "--pop-size", type=int, default=100, help="The " "population size"
    )

    opt_cmd.add_argument(
        "--n-generations", type=int, default=100, help="The number of generations"
    )

    opt_cmd.add_argument(
        "--outdir",
        default="./results-fuselage-optimization",
        help="The results will be saved here",
    )

    args = parser.parse_args()

    with open(args.parameters_map, "r") as params_map_file:
        parameters = json.load(params_map_file)

    parameters_index_side_by_side = {
        0: ["TailDiameter"],
        1: ["Length"],
        2: ["FloorHeight"],
        3: ["MiddleLength"],
        4: ["SphereDiameter"],
        5: ["Seat1FB", "Seat2FB"],
    }

    parameters_index_front_to_back = {
        0: ["TailDiameter"],
        1: ["Length"],
        2: ["FloorHeight"],
        3: ["MiddleLength"],
        4: ["SphereDiameter"],
        5: ["Seat1FB"],
        6: ["Seat2FB"],
    }

    xl_side_by_side = np.array([100, 1500, 130, 200, 1300, 750])
    xu_side_by_side = np.array([200, 2000, 150, 400, 1520, 790])

    xl_front_to_back = np.array([100, 1800, 110, 200, 800, 610, 610])
    xu_front_to_back = np.array([300, 3000, 150, 2000, 1500, 2500, 2500])

    design_in_creo = SymbenchDesignInCREO(
        parameters_map=parameters, assembly_path=args.asm
    )

    if args.seats_config == "side_by_side":
        params_set = {"Seat1LR": 210, "Seat2LR": -210}
        design_in_creo.logger.info(
            "Setting seat LR displacement to +-210 for side by side config"
        )

    else:
        params_set = {"Seat1LR": 0, "Seat2LR": 0}
        design_in_creo.logger.info(
            "Setting seat LR displacement to 0 for front to back config"
        )

    design_in_creo.apply_params(params_set)

    fuse_problem = FuselageOptimizationProblem(
        design_in_creo=design_in_creo,
        parameters_index=parameters_index_side_by_side
        if args.seats_config == "side_by_side"
        else parameters_index_front_to_back,
        xu=xu_side_by_side if args.seats_config == "side_by_side" else xu_front_to_back,
        xl=xl_side_by_side if args.seats_config == "side_by_side" else xl_front_to_back,
    )

    ngsa2 = NSGA2(pop_size=args.pop_size)

    out = optimize(fuse_problem, algorithm=ngsa2, n_generations=args.n_generations)

    savedir = create_directory(args.outdir)
    suffix = time.strftime("%b_%d_%Y_%H_%M_%S", time.localtime())
    with open(
        savedir / f"results_{suffix}.pkl",
        "wb",
    ) as pklfile:
        pickle.dump({"X": out.X, "F": out.F}, pklfile)

    pareto_csv_dict = get_pareto_csv_dict(fuse_problem.parameters_index, out.X, out.F)

    with open(savedir / f"results{suffix}_{args.seats_config}", "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=pareto_csv_dict[0].keys())
        writer.writeheader()
        writer.writerows(pareto_csv_dict)
