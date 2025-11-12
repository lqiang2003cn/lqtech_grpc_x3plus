import x3plus_pb2_grpc as x3plus_pb2_grpc
import x3plus_pb2 as x3plus_pb2
import grpc
from concurrent import futures
import logging
from x3plus_serial import Rosmaster
import numpy as np
import time


# RouteGuideServicer provides an implementation of the methods of the RouteGuide service.
class RosmasterServices(x3plus_pb2_grpc.RosmasterServices):

    def __init__(self):
        super().__init__()

        # joint name map to s_id:
        self.joint_name_to_sid_map ={
            "arm_joint1":1
        }

        # initalize Rosmaster serial comm class
        print("service initializing")

        self.serial = Rosmaster()
        self.serial.create_receive_threading()
        print(f"current batter voltage is: {self.serial.get_battery_voltage()}")

        print("service initialized")

    def SayHello(self, request, context):
        return x3plus_pb2.HelloReply(message=f"Hello, {request.name}")
    
    def SetSingleJointPosition(self, request:x3plus_pb2.SingleJointPositionRequest, context):
        print(f"joint value is: {request.joint_value}")
        joint_name = request.joint_name
        joint_value = request.joint_value

        before_set_cmd = self.serial.get_uart_servo_angle_array()
        while np.any(np.array(before_set_cmd)==-1):
            print("waiting")
            before_set_cmd = self.serial.get_uart_servo_angle_array()
            time.sleep(0.0001)
        print(before_set_cmd)

        target_angles = before_set_cmd.copy()
        target_angles[0] = joint_value

        if target_angles == before_set_cmd:
            return x3plus_pb2.SingleJointPositionResponse(result="OK")

        self.serial.set_uart_servo_angle_array(angle_s=target_angles, run_time=1000)

        after_set_cmd = self.serial.get_uart_servo_angle_array()
        while after_set_cmd!=target_angles:
            print("waiting for execution to complete")
            after_set_cmd = self.serial.get_uart_servo_angle_array()
            time.sleep(0.0001)
        print(f"after setting angles: {after_set_cmd}")

        # self.serial.set_uart_servo_angle(self.joint_name_to_sid_map[joint_name],joint_value,run_time=1000)
        return x3plus_pb2.SingleJointPositionResponse(result="OK")

def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    x3plus_pb2_grpc.add_RosmasterServicesServicer_to_server(RosmasterServices(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    serve()