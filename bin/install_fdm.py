#!/usr/bin/env python
"""In a Linux machine, install the Flight Dynamics software from SWRI."""

import os
import shutil
import subprocess
import sys

FDM_DIR = "FlightDynamics"


class CloneFailed(Exception):
    pass


class ConfigureFailed(Exception):
    pass


class MakeFailed(Exception):
    pass


class FDMInstaller:
    def __init__(self, token):
        self.start_dir = os.getcwd()
        self.token = token

    def install(self):
        if not sys.platform.startswith("linux"):
            raise OSError("This code only works on linux operating system")
        self.clone()
        self.configure()
        self.make_install()
        self.health_check()

    def _get_clone_url(self):
        git_url = "git.isis.vanderbilt.edu/SwRI/flight-dynamics-model.git"
        os.system(f"echo https://GITLAB_ACCESS_TOKEN:{self.token}@{git_url}")
        return f"https://GITLAB_ACCESS_TOKEN:{self.token}@{git_url}"

    def clone(self):
        shutil.rmtree(FDM_DIR, ignore_errors=True)
        with subprocess.Popen(
            f"git clone {self._get_clone_url()} {FDM_DIR}", shell=True
        ) as clone_process:
            try:
                clone_process.wait(500)
            except subprocess.TimeoutExpired:
                raise CloneFailed("Cloning failed due to timeout")
            if clone_process.returncode != 0:
                raise CloneFailed(
                    f"Unknown error occured while cloning FDM repository. {clone_process.stderr}"
                )

    def configure(self):
        os.chdir(FDM_DIR)
        with subprocess.Popen(f"./configure", shell=True) as configure_process:
            try:
                configure_process.wait(500)
            except subprocess.TimeoutExpired:
                raise ConfigureFailed("Configure Failed due to time out")
            if configure_process.returncode != 0:
                raise ConfigureFailed("Unknown error occured while confuguring FDM")

    def make_install(self):
        with subprocess.Popen(f"make clean install", shell=True) as make_process:
            try:
                make_process.wait(500)
            except subprocess.TimeoutExpired:
                raise MakeFailed("Make Failed due to time out")
            if make_process.returncode != 0:
                raise MakeFailed("Unknown error occured while installing FDM")
            os.system("mv bin/new_fdm /usr/bin/new_fdm")

    def health_check(self):
        pass  # ToDo: Manually verified for now, can incorporate health check later

    def cleanup(self):
        shutil.rmtree(FDM_DIR)
        os.chdir(self.start_dir)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description="The FDM tool installer")
    parser.add_argument("token", metavar="TOKEN", help="The gitlab access token")
    args = parser.parse_args()

    FDMInstaller(args.token).install()
