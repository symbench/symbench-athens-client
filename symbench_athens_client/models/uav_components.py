from symbench_athens_client.models.component import (
    ESC,
    GPS,
    Autopilot,
    Battery,
    CarbonFiberPlate,
    Flange,
    Hub,
    Instrument_Battery,
    Motor,
    Orient,
    Propeller,
    Receiver,
    Sensor,
    Servo,
    Wing,
    build_components,
    build_components_of_class,
    build_tubes,
)

ALL_FLANGES = ["0394_para_flange"]
ALL_TUBES = ["0281OD_para_tube", "0394OD_para_tube"]
ALL_HUBS = [
    "0394od_para_hub_2",
    "0394od_para_hub_3",
    "0394od_para_hub_4",
    "0394od_para_hub_5",
    "0394od_para_hub_6",
]
ALL_ORIENTS = ["Orient"]
ALL_CFPS = ["para_cf_fplate"]
CORPUS = "uav"

Batteries = build_components(Battery, CORPUS)
Propellers = build_components(Propeller, CORPUS)
Motors = build_components(Motor, CORPUS)
ESCs = build_components(ESC, CORPUS)
Instrument_Batteries = build_components(Instrument_Battery, CORPUS)
Wings = build_components(Wing, CORPUS)
GPSes = build_components(GPS, CORPUS)
Servos = build_components(Servo, CORPUS)
Receivers = build_components(Receiver, CORPUS)
Sensors = build_components(Sensor, CORPUS)
Autopilots = build_components(Autopilot, CORPUS)
# # Begin Parametric Components
Orients = build_components_of_class(Orient, ALL_ORIENTS, CORPUS)
Flanges = build_components_of_class(Flange, ALL_FLANGES, CORPUS)
Tubes = build_tubes(ALL_TUBES, CORPUS)
Hubs = build_components_of_class(Hub, ALL_HUBS, CORPUS)
CFPs = build_components_of_class(CarbonFiberPlate, ALL_CFPS, CORPUS)
