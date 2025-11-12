import x3plus_pb2_grpc as x3plus_pb2_grpc
import x3plus_pb2 as x3plus_pb2
import grpc
from concurrent import futures
import logging
from x3plus_serial import Rosmaster


# RouteGuideServicer provides an implementation of the methods of the RouteGuide service.
class RosmasterServices(x3plus_pb2_grpc.RosmasterServices):

    def __init__(self):
        super().__init__()

        # initalize Rosmaster serial comm class
        serial = Rosmaster()
        serial.create_receive_threading()
        print(f"current batter voltage is: {serial.get_battery_voltage()}")

        print("service initialized")

    def SayHello(self, request, context):
        return x3plus_pb2.HelloReply(message=f"Hello, {request.name}")
    
    def SetSingleJointPosition(self, request:x3plus_pb2.SingleJointPositionRequest, context):
        print(f"joint value is: {request.joint_value}")
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