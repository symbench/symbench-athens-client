from symbench_athens_client.models.fd_metrics import FDMFlightMetric
from symbench_athens_client.tests.utils import get_test_file_path


class TestFDMetrics:
    def test_non_existing_trim_states(self):
        non_existent_file_loc = get_test_file_path("no_trim_state_metrics.out")
        fdm_flight_metric = FDMFlightMetric.from_fd_metrics(non_existent_file_loc)
        fdm_flight_metric_dict = fdm_flight_metric.dict()
        assert all(val == 0.0 for val in fdm_flight_metric_dict.values())
