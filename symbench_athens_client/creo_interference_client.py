import json
from json import JSONDecodeError

import requests

INTEFERENCE_ENDPOINT = "/symbench-creoson"

INTERFERENCE_COMMAND = "interference"


class SymbenchCreoInterferenceClient:
    """Client interface to the interference server.

    Parameters
    ----------
    ip: str, default="http://localhost"
        The url of the Interference Server
    port: int, default=8000
        The port number for the interference Server
    """

    def __init__(self, ip_address="localhost", port=8000):
        self.server = f"http://{ip_address}:{port}{INTEFERENCE_ENDPOINT}"

    def get_global_interferences(self, assembly_path=None):
        """Given an assembly path, find global interferences."""
        data = {
            "command": INTERFERENCE_COMMAND,
            "function": "global_interference",
            "data": {"assembly_path": assembly_path},
        }

        return self._post(data)

    def _post(self, body):
        """Post to the interference server, and get response as JSON."""
        try:
            r = requests.post(self.server, data=json.dumps(body))
        except requests.exceptions.RequestException as e:
            raise ConnectionError(e)

        if r.status_code != 200:
            raise ConnectionError("Status code : {}".format(r.status_code))

        try:
            json_result = r.json()
        except TypeError:
            raise JSONDecodeError("Cannot decode JSON, creoson result invalid.")

        if "status" not in json_result.keys():
            raise KeyError("Missing `status` in creoson result.")

        if "error" not in json_result["status"].keys():
            raise KeyError("Missing `error` in status' creoson's result.")

        status = json_result["status"]["error"]
        if status:
            error_msg = json_result["status"]["message"]
            raise RuntimeError(error_msg)

        return json_result.get("data", None)
