import pytest

from symbench_athens_client.athens_client import SymbenchAthensClient
from symbench_athens_client.models.designs import QuadSpiderCopter
from symbench_athens_client.models.jobs import clearComponents
from symbench_athens_client.workflow import WorkFlow


@pytest.mark.skip
class TestWorkflow:
    @pytest.fixture(scope="session")
    def workflow_instance(self):
        client = SymbenchAthensClient(
            jenkins_url="http://localhost:8080",
            username="symcps",
            password="symcps2021",
        )
        wf = WorkFlow(client)
        return wf

    @pytest.mark.slow
    def test_clone_and_clear(self, workflow_instance):
        design = QuadSpiderCopter()
        workflow_instance.run(
            design,
            [clearComponents],
            build_params={"clearComponents": {"DesignName": design.name}},
            clone=True,
        )
