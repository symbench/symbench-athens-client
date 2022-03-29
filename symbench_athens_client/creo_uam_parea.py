"""Utility module to execute ProjectedArea calculation CREO MapKeys"""
import glob
import os
from pathlib import Path

import creopyson

PROJECTED_AREA_MAP_KEY = """"""


class MapKeysExecutor:
    """Execute a MapKey script in CREO using CREOSON(via. creopyson).

    Parameters
    ----------
    map_key: str
        The MapKeys string

    creoson_client: creopyson.Client instance
        The creopyson client
    """

    def __init__(self, mapkey, creoson_client):
        self.mapkey = mapkey
        self.creoson_client = creoson_client

    def execute(self, delay=0):
        """Execute the MapKeyScript."""
        self.creoson_client.interface_mapkey(self.mapkey, delay=delay)


class UAMProjectedAreaCalculator(MapKeysExecutor):
    """Calculate projected area for a UAM"""

    OUTFILES = ["proj_area_xy.txt"]

    def __init__(self, creoson_client):
        super().__init__(mapkey=PROJECTED_AREA_MAP_KEY, creoson_client=creoson_client)

        self.creo_working_dir = Path(self.creoson_client.creo_pwd()).resolve()

    def _get_path_in_working_dir(self, filename: str) -> Path:
        """Get path of a filename in creo's working directory."""
        return self.creo_working_dir / filename

    def _poll_and_delete_outputs(self):
        for outfile in self.OUTFILES:
            all_outfiles = [outfile] + glob.glob(
                str(self._get_path_in_working_dir(outfile)) + ".*"
            )
            print(all_outfiles)
            for of in all_outfiles:
                of_path = self._get_path_in_working_dir(of)
                if of_path.exists():
                    os.remove(of_path)

    def _wait_for_out_files(self):
        pass

    def _get_projected_area(self):
        pass

    def execute(self, delay=0):
        self._poll_and_delete_outputs()


if __name__ == "__main__":
    client = creopyson.Client(ip_adress="localhost", port=9056)
    client.connect()

    parea_calculator = UAMProjectedAreaCalculator(creoson_client=client)

    print(parea_calculator.execute())
