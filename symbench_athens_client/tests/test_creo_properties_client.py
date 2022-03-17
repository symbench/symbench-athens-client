import os

import pytest

from symbench_athens_client.creo_properties_client import SymbenchCreoPropertiesClient


@pytest.mark.skipif(os.environ.get("CI"), reason="Skip in CI.")
@pytest.mark.slow
class TestInterferenceClient:
    @pytest.fixture(scope="session")
    def creo_props_client(self):
        return SymbenchCreoPropertiesClient(ip_address="localhost", port=8000)

    def test_global_interference(self, creo_props_client):
        assert creo_props_client.get_global_interferences()

    def test_get_massprops(self, creo_props_client):
        assert creo_props_client.get_massproperties()
