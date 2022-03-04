from symbench_athens_client.models.component import (
    Battery,
    BatteryController,
    Beam,
    Beam_Cap,
    Cylinder,
    Cylinder_Flip,
    Flange,
    Fuselage,
    Hub,
    Motor,
    NACA_Port_Connector,
    Orient,
    Passenger,
    Propeller,
    Wing,
    build_components,
    build_components_of_class,
    build_tubes,
)

ALL_FLANGES = ["0394_para_flange", "0281_para_flange"]
ALL_HUBS = [
    "0394od_para_hub_2",
    "0394od_para_hub_3",
    "0394od_para_hub_4",
    "0394od_para_hub_5",
    "0394od_para_hub_6",
]
ALL_TUBES = ["0394OD_para_tube", "0281OD_para_tube"]
CORPUS = "uam"

Batteries = build_components(Battery, CORPUS)
Propellers = build_components(Propeller, CORPUS)
Motors = build_components(Motor, CORPUS)
Wings = build_components(Wing, CORPUS)
Beam_Caps = build_components(Beam_Cap, CORPUS)
NACA_Port_Connectors = build_components(NACA_Port_Connector, CORPUS)
BatteryControllers = build_components(BatteryController, CORPUS)
Orients = build_components(Orient, CORPUS)
Cylinders = build_components(Cylinder, CORPUS)
Fuselages = build_components(Fuselage, CORPUS)
Passengers = build_components(Passenger, CORPUS)
Beams = build_components(Beam, CORPUS)
Cylinder_Flips = build_components(Cylinder_Flip, CORPUS)
# Begin Parametric Components
Flanges = build_components_of_class(Flange, ALL_FLANGES, CORPUS)
Hubs = build_components_of_class(Hub, ALL_HUBS, CORPUS)
Tubes = build_tubes(ALL_TUBES, CORPUS)
