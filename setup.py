import os

from setuptools import setup

with open(os.path.join(".", "requirements.txt")) as f:
    install_deps = [
        line.strip() if not line.startswith("--editable") else ""
        for line in f.readlines()
    ]
    install_deps.append("uav_analysis")

setup(
    name="symbench_athens_client",
    version="0.0.1",
    description="Python interface to the symbench athens server",
    author="Umesh Timalsina",
    author_email="umesh.timalsina@vanderbilt.edu",
    install_requires=install_deps,
    license="Apache-2.0",
    packages=["symbench_athens_client"],
    zip_safe=True,
    include_package_data=True,
)
