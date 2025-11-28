
import logging

import grpc
import x3plus_pb2 as msg_def
import x3plus_pb2_grpc as srv_def
import time


def run():
    with grpc.insecure_channel('localhost:50051') as channel:

        stub = srv_def.RosmasterServicesStub(channel)
        
        count = 1
        for i in range(count):
            print(f"---- iteration {i+1} / {count} ----")
            response = stub.getJointPositionArray(msg_def.Empty())
            print(f"client received: {response.joint_array}")

            target_angles = list(response.joint_array)
            target_angles[0] = 92  # Example modification
            
            response = stub.setJointPositionSingle(
                msg_def.SingleJointPositionRequest(
                    joint_name="arm_joint1",
                    joint_value=target_angles[0]
                )
            )
            print(f"Set joint position response: {response.result}")

            # response = stub.setJointPositionArray(
            #     msg_def.JointPosititonArray(
            #         joint_array=target_angles
            #     )
            # )
            # print(f"Set joint position response: {response.result}")

            # response = stub.setJointPositionArray(
            #     msg_def.JointPosititonArray(
            #         joint_array=target_angles
            #     )
            # )
            # print(f"Set joint position response: {response.result}")



if __name__ == "__main__":
    logging.basicConfig()
    start_time = time.perf_counter()
    run()
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Execution took {elapsed_time:.6f} seconds")
