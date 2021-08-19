from typing import ClassVar

from symbench_athens_client.models.components import Batteries, Motors, Propellers
from symbench_athens_client.models.designs import QuadCopter


class TurnigyGraphene5000MAHQuadCopter(QuadCopter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Change Battery
        self.battery_0 = Batteries.TurnigyGraphene5000mAh4S75C

        # Change Motors
        self.motor_0 = Motors.t_motor_AT2312KV1400
        self.motor_1 = Motors.t_motor_AT2312KV1400
        self.motor_2 = Motors.t_motor_AT2312KV1400
        self.motor_3 = Motors.t_motor_AT2312KV1400

        # Change Propellers
        self.propeller_0 = Propellers.apc_propellers_6x4EP
        self.propeller_1 = Propellers.apc_propellers_6x4E
        self.propeller_2 = Propellers.apc_propellers_6x4EP
        self.propeller_3 = Propellers.apc_propellers_6x4E


class Batt60006S_Prop10x4_5MR_MotMN3508KV380QuadCopter(QuadCopter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Motors
        self.motor_0 = Motors.t_motor_MN3508KV380
        self.motor_1 = Motors.t_motor_MN3508KV380
        self.motor_2 = Motors.t_motor_MN3508KV380
        self.motor_3 = Motors.t_motor_MN3508KV380

        # Propellers
        self.propeller_0 = Propellers.apc_propellers_10x4_5MRP
        self.propeller_1 = Propellers.apc_propellers_10x4_5MR
        self.propeller_2 = Propellers.apc_propellers_10x4_5MR
        self.propeller_3 = Propellers.apc_propellers_10x4_5MRP

        # Battery
        self.battery_0 = Batteries.TurnigyGraphene6000mAh6S75C
