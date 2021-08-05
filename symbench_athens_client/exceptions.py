class JobFailedError(Exception):
    """Error to be raised when a job fails."""


class ParametersMismatchError(Exception):
    """Error to be raised when there are insufficient parameters for a build."""
