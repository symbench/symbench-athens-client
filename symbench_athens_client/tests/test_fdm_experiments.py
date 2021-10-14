import os
import shutil
import tempfile
import zipfile
from pathlib import Path

import minio
import pytest

from symbench_athens_client.fdm_experiments import get_experiments_by_name
from symbench_athens_client.models.components import Batteries, Motors, Propellers


@pytest.mark.slow
class TestFDMExperiments:
    @pytest.fixture(autouse=True, scope="session")
    def download_testbenches(self):
        client = minio.Minio(
            access_key=os.environ["MINIO_ACCESS_KEY"],
            secret_key=os.environ["MINIO_SECRET_KEY"],
            endpoint=os.environ["MINIO_ENDPOINT"],
        )
        old_pwd = os.getcwd()

        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            client.fget_object("fdmdata", "FDMdata.zip", "FDMdata.zip")
            os.getcwd()
            with zipfile.ZipFile("FDMdata.zip", "r") as zip_file:
                for member in zip_file.namelist():
                    if "propellers" in member or "testbenches" in member:
                        zip_file.extract(member, Path(__file__).parent / ".." / "..")

        os.chdir(old_pwd)
        yield
        shutil.rmtree(Path(__file__).parent / ".." / ".." / "propellers")
        shutil.rmtree(Path(__file__).parent / ".." / ".." / "testbenches")

    def test_turingy_graphene_6000mah(self):
        expr = get_experiments_by_name("ExperimentOnTurnigyGraphene6000MAHQuadCopter")
        expr.start_new_session()
        results = expr.run_for(
            parameters={
                "arm_length": 400,
                "support_length": 20,
                "batt_mount_z_offset": 30,
                "r": 100.0,
            },
            requirements={
                "requested_vertical_speed": -2,
                "requested_lateral_speed": 40,
            },
        )
        assert results["TotalPathScore"] == 1565.0

    def test_on_quadcopter_5(self):
        expr = get_experiments_by_name("ExperimentOnQuadCopter_5")
        expr.start_new_session()

        results = expr.run_for(
            parameters={
                "arm_length": 324,
                "support_length": 2.11,
                "batt_mount_z_offset": 43.6842105263158,
                "r": 360.0,
            },
            requirements={
                "requested_vertical_speed": -2,
                "requested_lateral_speed": 50,
            },
        )

        assert results["TotalPathScore"] == 1582

    def test_on_quadcopter_5_light(self):
        expr = get_experiments_by_name("ExperimentOnQuadCopter_5Light")
        expr.start_new_session()

        results = expr.run_for(
            parameters={
                "arm_length": 325,
                "support_length": 1,
                "batt_mount_z_offset": 1,
                "r": 360.0,
            },
            requirements={
                "requested_vertical_speed": -2,
                "requested_lateral_speed": 50,
            },
        )

        assert results["TotalPathScore"] == 1582

    def test_fd_execution_variable_battery_quad(self):
        expr = get_experiments_by_name("QuadCopterVariableBatteryPropExperiment")
        expr.start_new_session()
        expr.design.motor_0 = Motors["t_motor_MN4012KV400"]
        expr.design.motor_1 = Motors["t_motor_MN4012KV400"]
        expr.design.motor_2 = Motors["t_motor_MN4012KV400"]
        expr.design.motor_3 = Motors["t_motor_MN4012KV400"]

        expr.battery = Batteries["TurnigyGraphene6000mAh6S75C"]

        expr.propeller = Propellers["apc_propellers_16x4EP"]
        assert (
            expr.design.propeller_0
            == Propellers["apc_propellers_16x4EP"]
            == expr.design.propeller_2
        )
        assert (
            expr.design.propeller_1
            == Propellers["apc_propellers_16x4E"]
            == expr.design.propeller_3
        )

        results = expr.run_for(
            parameters={
                "arm_length": 400,
                "support_length": 20,
                "batt_mount_z_offset": 30,
                "r": 100.0,
            },
            requirements={
                "requested_vertical_speed": -2,
                "requested_lateral_speed": 40,
            },
        )

        assert results["TotalPathScore"] == 1565.0

    def test_fd_execution_can_run_for(self):
        expr = get_experiments_by_name("QuadCopterVariableBatteryPropExperiment")
        assert expr.can_run_for("apc_propellers_16x4EP")
        assert expr.can_run_for("apc_propellers_16x4E")
        assert not expr.can_run_for("apc_propellers_17x10N")
