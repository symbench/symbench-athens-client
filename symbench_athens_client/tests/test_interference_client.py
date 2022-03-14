import os

import pytest

from symbench_athens_client.creo_interference_client import (
    SymbenchCreoInterferenceClient,
)


@pytest.mark.skipif(os.environ.get("CI"), reason="Skip in CI.")
@pytest.mark.slow
class TestInterferenceClient:
    @pytest.fixture(scope="session")
    def intf_client(self):
        return SymbenchCreoInterferenceClient(ip_address="localhost", port=8000)

    def test_global_interference(self, intf_client):
        assert intf_client.get_global_interferences()
