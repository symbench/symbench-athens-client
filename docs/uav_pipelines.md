# UAV Workflow Pipelines

## GeometryV1

The `Geometry_V1` TestBench for UAV_Workflows.



### Jenkins Design Variables and Defaults (Assuming a QuadCopter seed design):
| NumSamples | PETName | graphGUID | DesignVars |
|-----|-----|-----|-----|
| 1 | /D_Testing/PET/Geom_V1 | QuadCopter | "Q_Position=1.0,1.0 Q_Velocity=1.0,1.0 Q_Angular_Velocity=1.0,1.0 Q_Angles=1.0,1.0 R=1.0,1.0 Length_0=220.0,220.0 Length_1=95.0,95.0 Length_8=0.0,0.0 Length_9=0.0,0.0" |





## HoverCalc

The `HoverCalc_V1` TestBench for UAV_Workflows.



### Jenkins Design Variables and Defaults (Assuming a QuadCopter seed design):
| NumSamples | PETName | graphGUID | DesignVars |
|-----|-----|-----|-----|
| 1 | /D_Testing/PET/HoverCalc_V1 | QuadCopter | "Q_Position=1.0,1.0 Q_Velocity=1.0,1.0 Q_Angular_Velocity=1.0,1.0 Q_Angles=1.0,1.0 R=1.0,1.0 Length_0=220.0,220.0 Length_1=95.0,95.0 Length_8=0.0,0.0 Length_9=0.0,0.0" |





## TrimSteadyFlight

The Trim Steady Flight, using `analysis_type=2` in `FlightDyanmics`.


 Parameters that can't be changed are listed below:

| name | Jenkins Name | default | description |
|-----|-----|-----|-----|
| analysis_type | Analysis_Type | 2 | None |



### Jenkins Design Variables and Defaults (Assuming a QuadCopter seed design):
| NumSamples | PETName | graphGUID | DesignVars |
|-----|-----|-----|-----|
| 1 | /D_Testing/PET/FlightDyn_V1 | QuadCopter | "Q_Position=1.0,1.0 Q_Velocity=1.0,1.0 Q_Angular_Velocity=1.0,1.0 Q_Angles=1.0,1.0 R=1.0,1.0 Length_0=220.0,220.0 Length_1=95.0,95.0 Length_8=0.0,0.0 Length_9=0.0,0.0 Analysis_Type=2,2" |





## InitialConditionsFlight

The InitialConditions Flight, using `analysis_type=1` in `FlightDynamics`.


 Parameters that can't be changed are listed below:

| name | Jenkins Name | default | description |
|-----|-----|-----|-----|
| analysis_type | Analysis_Type | 1 | None |



### Jenkins Design Variables and Defaults (Assuming a QuadCopter seed design):
| NumSamples | PETName | graphGUID | DesignVars |
|-----|-----|-----|-----|
| 1 | /D_Testing/PET/FlightDyn_V1 | QuadCopter | "Q_Position=1.0,1.0 Q_Velocity=1.0,1.0 Q_Angular_Velocity=1.0,1.0 Q_Angles=1.0,1.0 R=1.0,1.0 Length_0=220.0,220.0 Length_1=95.0,95.0 Length_8=0.0,0.0 Length_9=0.0,0.0 Analysis_Type=1,1" |





## StraightLineFlight

The Straight line flight, subclasses `FlightPathFlight`, `analysis_type=3`, `flight_path=1`.


 Parameters that can be changed are listed below:

| name | Jenkins Name | default | description |
|-----|-----|-----|-----|
| requested_lateral_speed | Requested_Lateral_Speed | 10.0 | The requested lateral speed |
| requested_vertical_speed | Requested_Vertical_Speed | 1.0 | The requested vertical speed |


 Parameters that can't be changed are listed below:

| name | Jenkins Name | default | description |
|-----|-----|-----|-----|
| analysis_type | Analysis_Type | 3 | None |
| flight_path | Flight_Path | 1 | None |



### Jenkins Design Variables and Defaults (Assuming a QuadCopter seed design):
| NumSamples | PETName | graphGUID | DesignVars |
|-----|-----|-----|-----|
| 1 | /D_Testing/PET/FlightDyn_V1 | QuadCopter | "Q_Position=1.0,1.0 Q_Velocity=1.0,1.0 Q_Angular_Velocity=1.0,1.0 Q_Angles=1.0,1.0 R=1.0,1.0 Length_0=220.0,220.0 Length_1=95.0,95.0 Length_8=0.0,0.0 Length_9=0.0,0.0 Requested_Lateral_Speed=10.0,10.0 Requested_Vertical_Speed=1.0,1.0 Analysis_Type=3,3 Flight_Path=1,1" |





## CircularFlight

The Circular flight, subclasses `FlightPathFlight`, `analysis_type=3`, `flight_path=3`.


 Parameters that can be changed are listed below:

| name | Jenkins Name | default | description |
|-----|-----|-----|-----|
| requested_lateral_speed | Requested_Lateral_Speed | 10.0 | The requested lateral speed |
| requested_vertical_speed | Requested_Vertical_Speed | 1.0 | The requested vertical speed |


 Parameters that can't be changed are listed below:

| name | Jenkins Name | default | description |
|-----|-----|-----|-----|
| analysis_type | Analysis_Type | 3 | None |
| flight_path | Flight_Path | 3 | None |



### Jenkins Design Variables and Defaults (Assuming a QuadCopter seed design):
| NumSamples | PETName | graphGUID | DesignVars |
|-----|-----|-----|-----|
| 1 | /D_Testing/PET/FlightDyn_V1 | QuadCopter | "Q_Position=1.0,1.0 Q_Velocity=1.0,1.0 Q_Angular_Velocity=1.0,1.0 Q_Angles=1.0,1.0 R=1.0,1.0 Length_0=220.0,220.0 Length_1=95.0,95.0 Length_8=0.0,0.0 Length_9=0.0,0.0 Requested_Lateral_Speed=10.0,10.0 Requested_Vertical_Speed=1.0,1.0 Analysis_Type=3,3 Flight_Path=3,3" |





## RiseAndHoverFlight

The rise and hover flight, subclasses `FlightPathFlight`, `analysis_type=3`, `flight_path=4`.


 Parameters that can be changed are listed below:

| name | Jenkins Name | default | description |
|-----|-----|-----|-----|
| requested_lateral_speed | Requested_Lateral_Speed | 10.0 | The requested lateral speed |
| requested_vertical_speed | Requested_Vertical_Speed | 1.0 | The requested vertical speed |


 Parameters that can't be changed are listed below:

| name | Jenkins Name | default | description |
|-----|-----|-----|-----|
| analysis_type | Analysis_Type | 3 | None |
| flight_path | Flight_Path | 4 | None |



### Jenkins Design Variables and Defaults (Assuming a QuadCopter seed design):
| NumSamples | PETName | graphGUID | DesignVars |
|-----|-----|-----|-----|
| 1 | /D_Testing/PET/FlightDyn_V1 | QuadCopter | "Q_Position=1.0,1.0 Q_Velocity=1.0,1.0 Q_Angular_Velocity=1.0,1.0 Q_Angles=1.0,1.0 R=1.0,1.0 Length_0=220.0,220.0 Length_1=95.0,95.0 Length_8=0.0,0.0 Length_9=0.0,0.0 Requested_Lateral_Speed=0.0,0.0 Requested_Vertical_Speed=1.0,1.0 Analysis_Type=3,3 Flight_Path=4,4" |





## RacingOvalFlight

The racing oval flight, subclasses FlightPathFlight, `analysis_type=3`, `flight_path=5`.


 Parameters that can be changed are listed below:

| name | Jenkins Name | default | description |
|-----|-----|-----|-----|
| requested_lateral_speed | Requested_Lateral_Speed | 10.0 | The requested lateral speed |
| requested_vertical_speed | Requested_Vertical_Speed | 1.0 | The requested vertical speed |


 Parameters that can't be changed are listed below:

| name | Jenkins Name | default | description |
|-----|-----|-----|-----|
| analysis_type | Analysis_Type | 3 | None |
| flight_path | Flight_Path | 5 | None |



### Jenkins Design Variables and Defaults (Assuming a QuadCopter seed design):
| NumSamples | PETName | graphGUID | DesignVars |
|-----|-----|-----|-----|
| 1 | /D_Testing/PET/FlightDyn_V1 | QuadCopter | "Q_Position=1.0,1.0 Q_Velocity=1.0,1.0 Q_Angular_Velocity=1.0,1.0 Q_Angles=1.0,1.0 R=1.0,1.0 Length_0=220.0,220.0 Length_1=95.0,95.0 Length_8=0.0,0.0 Length_9=0.0,0.0 Requested_Lateral_Speed=10.0,10.0 Requested_Vertical_Speed=1.0,1.0 Analysis_Type=3,3 Flight_Path=5,5" |





## FlightPathsAll

Run all the FlightPathFlights' Analysis (1, 3, 4 and 5)


 Parameters that can be changed are listed below:

| name | Jenkins Name | default | description |
|-----|-----|-----|-----|
| requested_lateral_speed | Requested_Lateral_Speed | 10.0 | The requested lateral speed |
| requested_vertical_speed | Requested_Vertical_Speed | 1.0 | The requested vertical speed |



### Jenkins Design Variables and Defaults (Assuming a QuadCopter seed design):
| graphGUID | PETName | NumSamples | DesignVars |
|-----|-----|-----|-----|
| QuadCopter | /D_Testing/PET/FlightDyn_V1_AllPaths | 1 | "Length_0=220.0,220.0 Length_1=95.0,95.0 Length_8=0.0,0.0 Length_9=0.0,0.0 Q_Angles_1=1.0,1.0 Q_Velocity_1=1.0,1.0 Q_Position_1=1.0,1.0 Q_Angular_Velocity_1=1.0,1.0 R_1=1.0,1.0 Requested_Vertical_Speed_1=0,0 Requested_Lateral_Speed_1=10.0,10.0 Q_Angles_3=1.0,1.0 Q_Velocity_3=1.0,1.0 Q_Position_3=1.0,1.0 Q_Angular_Velocity_3=1.0,1.0 R_3=1.0,1.0 Requested_Vertical_Speed_3=0,0 Requested_Lateral_Speed_3=10.0,10.0 Q_Angles_4=1.0,1.0 Q_Velocity_4=1.0,1.0 Q_Position_4=1.0,1.0 Q_Angular_Velocity_4=1.0,1.0 R_4=1.0,1.0 Requested_Vertical_Speed_4=1.0,1.0 Requested_Lateral_Speed_4=0,0 Q_Angles_5=1.0,1.0 Q_Velocity_5=1.0,1.0 Q_Position_5=1.0,1.0 Q_Angular_Velocity_5=1.0,1.0 R_5=1.0,1.0 Requested_Vertical_Speed_5=0,0 Requested_Lateral_Speed_5=10.0,10.0" |
