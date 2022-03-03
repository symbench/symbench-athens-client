import logging
import os

import pytest

from symbench_athens_client.athens_graphdb_client import SymbenchAthensGraphDBClient
from symbench_athens_client.models.uam_designs import Rake


def is_uav_corpus():
    return os.environ.get("DB_CORPUS") == "uav"


def is_uam_corpus():
    return os.environ.get("DB_CORPUS") == "uam"


@pytest.mark.slow
@pytest.mark.skipif(os.environ.get("CI"), reason="skip in CI")
class TestGraphDBClient:
    @pytest.fixture(scope="session")
    def client(self):
        client = SymbenchAthensGraphDBClient(
            gremlin_url=os.environ.get("GREMLIN_URL"), log_level=logging.INFO
        )
        yield client
        client.close()

    @pytest.mark.skipif(not is_uam_corpus(), reason="Wrong corpus")
    def test_seed_uam_designs(self, client):
        assert "Rake" in client.get_all_design_names()

    @pytest.mark.skipif(not is_uav_corpus(), reason="Wrong corpus")
    def test_seed_uav_designs(self, client):
        assert "QuadCopter" in client.get_all_design_names()

    @pytest.mark.skipif(not is_uam_corpus(), reason="Wrong Corpus")
    def test_clone_clear_rake(self, client):
        design = Rake()
        client.clone_design(design)
        assert design.name in client.get_all_design_names()
        client.clear_design(design)
        assert design.name not in client.get_all_design_names()
