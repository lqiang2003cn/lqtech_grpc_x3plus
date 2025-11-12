
import logging

import grpc
import x3plus_pb2 as x3plus_pb2
import x3plus_pb2_grpc as x3plus_pb2_grpc
import time


def run():
    with grpc.insecure_channel('192.168.31.238:50051') as channel:
        stub = x3plus_pb2_grpc.RosmasterServicesStub(channel)
        response = stub.SetSingleJointPosition(x3plus_pb2.SingleJointPositionRequest(
            joint_name="arm_joint1",
            joint_value=31
        ))
        print(f"Greeter client received: {response.result}")


if __name__ == "__main__":
    logging.basicConfig()
    start_time = time.perf_counter()
    run()
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Execution took {elapsed_time:.6f} seconds")
