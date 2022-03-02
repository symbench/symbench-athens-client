import warnings

warnings.warn(
    f"This {__name__} is strictly here for backwards compatibility "
    f"and will be removed in the future. "
    f"Please update your code base to incorporate the imports from "
    f"symbench_athens_client.models.uav_designs for UAV designs and "
    f"symbench_athens_client.models.uam_designs for UAM designs.",
    category=DeprecationWarning,
    stacklevel=2,
)  # FixMe: A proper deprecation recipe should be used here

from symbench_athens_client.models.uam_designs import *
from symbench_athens_client.models.uav_designs import *
