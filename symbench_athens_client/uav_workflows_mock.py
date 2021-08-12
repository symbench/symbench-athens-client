from symbench_athens_client.models.designs import SeedDesign
from symbench_athens_client.models.flight_modes import (
    CircularFlight,
    FlightModeSettings,
    InitialConditionsFlight,
    RacingOvalFlight,
    RiseAndHoverFlight,
    StraightLineFlight,
    TrimSteadyFlight,
)


def _merge_params_fd(design, analysis_mode, num_samples):
    assert isinstance(
        design, SeedDesign
    ), "Please provide a proper seed design instance"
    assert isinstance(
        analysis_mode, FlightModeSettings
    ), "Please provide a proper analysis setting instance"
    params = design.to_jenkins_parameters()
    params["DesignVars"] = (
        params["DesignVars"] + " " + analysis_mode.to_jenkins_parameters()["DesignVars"]
    )
    params["PETName"] = "/D_Testing/PET/FlightDyn_V1"
    params["graphGUID"] = design.name
    params["NumSamples"] = num_samples
    return params


def fly_with_initial_conditions(design, num_samples=1, requested_velocity=10.0):
    """Fly with initial conditions workflow

    Run the UAVWorkflows' flight dynamics test bench to execute a flight from initial conditions
    (Mock Implementation returning only jenkins parameters)

    Prefixed Settings for this FD workflow are: Analysis_Type is 1

    Parameters
    ----------
    design: symbench_athens_client.models.designs.SeedDesign
        The design to run this workflow on
    num_samples: int, default=1
        The number of samples to run for
    requested_velocity: float, default=10.0
        The requested velocity for this flight
    """
    initial_condition_flight = InitialConditionsFlight(
        requested_velocity=requested_velocity
    )
    print(initial_condition_flight.requested_velocity)
    return _merge_params_fd(design, initial_condition_flight, num_samples)


def fly_trim_steady(design, num_samples=1, requested_velocity=10.0):
    """Fly with initial conditions workflow

    Run the UAVWorkflows' flight dynamics test bench to perform a trim analysis to U = x(1) forward speed, level steady flight.
    (Mock Implementation returning only jenkins parameters)

    Prefixed Settings for this FD workflow are: Analysis_Type is 2
    Parameters
    ----------
    design: symbench_athens_client.models.designs.SeedDesign
        The design to run this workflow on
    num_samples: int, default=1
        The number of samples to run for
    requested_velocity: float, default=10.0
        The requested velocity for this run
    """
    trim_steady_flight = TrimSteadyFlight(requested_velocity=requested_velocity)

    return _merge_params_fd(design, trim_steady_flight, num_samples)


def fly_straight_line(design, num_samples=1, **kwargs):
    """Fly Circle workflow

    Run the UAVWorkflows' flight dynamics test bench to execute a straight line flight path
    (Mock Implementation returning only jenkins parameters)

    Prefixed Settings for this FD workflow are: Analysis_Type is 3, Flight_Path is 1.
    See the **kwargs below to see what can be requested.

    Parameters
    ----------
    design: symbench_athens_client.models.designs.SeedDesign
        The design to run this workflow on
    num_samples: int, default=1
        The number of samples to run for
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
    return _merge_params_fd(design, flight_mode, num_samples)


def fly_circle(design, num_samples=1, **kwargs):
    """Fly Circle workflow

    Run the UAVWorkflows' flight dynamics test bench to execute a circular flight path
    (Mock Implementation returning only jenkins parameters)

    Prefixed Settings for this FD workflow are: Analysis_Type is 3, Flight_Path is 3.
    See the **kwargs below to see what can be requested.

    Parameters
    ----------
    design: symbench_athens_client.models.designs.SeedDesign
        The design to run this workflow on
    num_samples: int, default=1
        The number of samples to run for
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
    return _merge_params_fd(design, circular_flight_mode, num_samples)


def fly_rise_and_hover(design, num_samples=1, **kwargs):
    """Fly Rise and Hover (i.e. Vertical Rise)

    Run the UAVWorkflows' flight dynamics test bench to execute a rise and hover
    (Mock Implementation returning only jenkins parameters)

    Prefixed Settings for this FD workflow are: Analysis_Type is 3, Flight_Path is 4.
    See the **kwargs below to see what can be requested.

    Parameters
    ----------
    design: symbench_athens_client.models.designs.SeedDesign
        The design to run this workflow on
    num_samples: int, default=1
        The number of samples to run for
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
    return _merge_params_fd(design, circular_flight_mode, num_samples)


def fly_racing_oval(design, num_samples=1, **kwargs):
    """Fly Racing Oval Flight

    Run the UAVWorkflows' flight dynamics test bench to execute a Racing Oval Flight
    (Mock Implementation returning only jenkins parameters)

    Prefixed Settings for this FD workflow are: Analysis_Type is 3, Flight_Path is 5.
    See the **kwargs below to see what can be requested.

    Parameters
    ----------
    design: symbench_athens_client.models.designs.SeedDesign
        The design to run this workflow on
    num_samples: int, default=1
        The number of samples to run for
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
    racing_oval_flight_mode = RacingOvalFlight(**kwargs)
    return _merge_params_fd(design, racing_oval_flight_mode, num_samples)
