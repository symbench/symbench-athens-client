from symbench_athens_client.models.designs import SeedDesign
from symbench_athens_client.models.uav_analysis import (
    CircularFlight,
    FlightDynamicsSettings,
    InitialConditionsFlight,
    RacingOvalFlight,
    RiseAndHoverFlight,
    StraightLineFlight,
    TrimSteadyFlight,
)


def _merge_params_fd(design, analysis_mode):
    assert isinstance(
        design, SeedDesign
    ), "Please provide a proper seed design instance"
    assert isinstance(
        analysis_mode, FlightDynamicsSettings
    ), "Please provide a proper analysis setting instance"
    params = design.to_jenkins_parameters()
    params["DesignVars"] = (
        params["DesignVars"] + " " + analysis_mode.to_jenkins_parameters()["DesignVars"]
    )
    params["PETName"] = "/D_Testing/PET/FlightDyn_V1"
    params["graphGUID"] = design.name
    params["NumSamples"] = 1
    return params


def fly_with_initial_conditions(design, requested_velocity=10.0):
    """Fly with initial conditions workflow

    Run the UAVWorkflows' flight dynamics test bench to execute a flight from initial conditions
    (Mock Implementation returning only jenkins parameters)

    Prefixed Settings for this FD workflow are: Analysis_Type is 1

    Parameters
    ----------
    design: symbench_athens_client.models.designs.SeedDesign
        The design to run this workflow on
    requested_velocity: float, default=10.0
        The requested velocity for this flight
    """
    initial_condition_flight = InitialConditionsFlight(
        requested_velocity=requested_velocity
    )
    return _merge_params_fd(design, initial_condition_flight)


def fly_trim_steady(design, requested_velocity=10.0):
    """Fly with initial conditions workflow

    Run the UAVWorkflows' flight dynamics test bench to perform a trim analysis to U = x(1) forward speed, level steady flight.
    (Mock Implementation returning only jenkins parameters)

    Prefixed Settings for this FD workflow are: Analysis_Type is 2
    Parameters
    ----------
    design: symbench_athens_client.models.designs.SeedDesign
        The design to run this workflow on
    requested_velocity: float, default=10.0
        The requested velocity for this run
    """
    trim_steady_flight = TrimSteadyFlight(requested_velocity=requested_velocity)

    return _merge_params_fd(design, trim_steady_flight)


def fly_straight_line(design, **kwargs):
    """Fly Circle workflow

    Run the UAVWorkflows' flight dynamics test bench to execute a straight line flight path
    (Mock Implementation returning only jenkins parameters)

    Prefixed Settings for this FD workflow are: Analysis_Type is 3, Flight_Path is 1.
    See the **kwargs below to see what can be requested.

    Parameters
    ----------
    design: symbench_athens_client.models.designs.SeedDesign
        The design to run this workflow on
    **kwargs:
        The KeyWord Arguments to the CircularFlight's constructor listed below:
        - 'requested_velocity',
        - 'requested_lateral_speed',
        - 'q_position',
        - 'q_velocity',
        - 'q_angluar_velocity',
        - 'q_angles',
        - 'r'

    See Also
    --------
    symbench_athens_client.models.uav_analysis
        The module with different flight path methods
    """
    flight_mode = StraightLineFlight(**kwargs)
    return _merge_params_fd(design, flight_mode)


def fly_circle(design, **kwargs):
    """Fly Circle workflow

    Run the UAVWorkflows' flight dynamics test bench to execute a circular flight path
    (Mock Implementation returning only jenkins parameters)

    Prefixed Settings for this FD workflow are: Analysis_Type is 3, Flight_Path is 3.
    See the **kwargs below to see what can be requested.

    Parameters
    ----------
    design: symbench_athens_client.models.designs.SeedDesign
        The design to run this workflow on
    **kwargs:
        The KeyWord Arguments to the CircularFlight's constructor listed below:
        - 'requested_velocity',
        - 'requested_lateral_speed',
        - 'q_position',
        - 'q_velocity',
        - 'q_angluar_velocity',
        - 'q_angles',
        - 'r'

    See Also
    --------
    symbench_athens_client.models.uav_analysis
        The module with different flight path methods
    """
    circular_flight_mode = CircularFlight(**kwargs)
    return _merge_params_fd(design, circular_flight_mode)


def fly_rise_and_hover(design, **kwargs):
    """Fly Rise and Hover (i.e. Vertical Rise)

    Run the UAVWorkflows' flight dynamics test bench to execute a rise and hover
    (Mock Implementation returning only jenkins parameters)

    Prefixed Settings for this FD workflow are: Analysis_Type is 3, Flight_Path is 4.
    See the **kwargs below to see what can be requested.

    Parameters
    ----------
    design: symbench_athens_client.models.designs.SeedDesign
        The design to run this workflow on
    **kwargs:
        The KeyWord Arguments to the CircularFlight's constructor listed below:
        - 'requested_velocity',
        - 'requested_lateral_speed', (this has no effect and is always set to zero)
        - 'q_position',
        - 'q_velocity',
        - 'q_angluar_velocity',
        - 'q_angles',
        - 'r'

    See Also
    --------
    symbench_athens_client.models.uav_analysis
        The module with different flight path methods
    """
    circular_flight_mode = RiseAndHoverFlight(**kwargs)
    return _merge_params_fd(design, circular_flight_mode)


def racing_oval_flight(design, **kwargs):
    racing_oval_flight_mode = RacingOvalFlight(**kwargs)
    return _merge_params_fd(design, racing_oval_flight_mode)
