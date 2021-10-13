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


class TurnigyGraphene6000MAHQuadCopter(QuadCopter):
    def __init__(self, *args, **kwargs):
        super(TurnigyGraphene6000MAHQuadCopter, self).__init__(*args, **kwargs)
        # Change Battery
        self.battery_0 = Batteries.TurnigyGraphene6000mAh6S75C

        # Change Motors
        self.motor_0 = Motors.t_motor_MN4012KV400
        self.motor_1 = Motors.t_motor_MN4012KV400
        self.motor_2 = Motors.t_motor_MN4012KV400
        self.motor_3 = Motors.t_motor_MN4012KV400

        # Change Propellers
        self.propeller_0 = Propellers.apc_propellers_16x4EP
        self.propeller_1 = Propellers.apc_propellers_16x4E
        self.propeller_2 = Propellers.apc_propellers_16x4EP
        self.propeller_3 = Propellers.apc_propellers_16x4E

        self.validate_propellers_directions()


class QuadCopter_5(QuadCopter):
    def __init__(self, *args, **kwargs):
        super(QuadCopter_5, self).__init__(*args, **kwargs)
        # Change Battery
        self.battery_0 = Batteries.TurnigyGraphene6000mAh6S75C

        # Change Motors
        self.motor_0 = Motors.t_motor_MN5208KV340
        self.motor_1 = Motors.t_motor_MN5208KV340
        self.motor_2 = Motors.t_motor_MN5208KV340
        self.motor_3 = Motors.t_motor_MN5208KV340

        # Change Propellers
        self.propeller_0 = Propellers.apc_propellers_18x5_5MRP
        self.propeller_1 = Propellers.apc_propellers_18x5_5MR
        self.propeller_2 = Propellers.apc_propellers_18x5_5MRP
        self.propeller_3 = Propellers.apc_propellers_18x5_5MR

        self.validate_propellers_directions()


class QuadCopter_5Light(QuadCopter):
    def __init__(self, *args, **kwargs):
        super(QuadCopter_5Light, self).__init__(*args, **kwargs)
        # Change Battery
        self.battery_0 = Batteries.TurnigyGraphene5000mAh6S75C

        # Change Motors
        self.motor_0 = Motors.t_motor_MN5208KV340
        self.motor_1 = Motors.t_motor_MN5208KV340
        self.motor_2 = Motors.t_motor_MN5208KV340
        self.motor_3 = Motors.t_motor_MN5208KV340

        # Change Propellers
        self.propeller_0 = Propellers.apc_propellers_18x5_5MRP
        self.propeller_1 = Propellers.apc_propellers_18x5_5MR
        self.propeller_2 = Propellers.apc_propellers_18x5_5MRP
        self.propeller_3 = Propellers.apc_propellers_18x5_5MR

        self.validate_propellers_directions()
