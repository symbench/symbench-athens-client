class JobFailedError(Exception):
    """Error to be raised when a job fails."""


class ParametersMismatchError(Exception):
    """Error to be raised when there are insufficient parameters for a build."""


class FDMFailedException(Exception):
    """Exception to be raised when the FDM process failed."""


class MissingExperimentError(Exception):
    """Exception to be raised when an experiment is missing."""


class PropellerAssignmentError(Exception):
    """Exception to be raised when there's an error in assigning propellers."""
