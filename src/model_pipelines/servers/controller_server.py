# server logic
import asyncio
from model_pipelines.proto.ControllerService_pb2_grpc import add_ControllerServiceServicer_to_server
from model_pipelines.controller import ControllerService  # choose autoscaling or not here
from model_pipelines.servers.server_runner import run_grpc_server

if __name__ == "__main__":
    asyncio.run(run_grpc_server(
        servicer_cls=ControllerService,
        add_servicer_fn=add_ControllerServiceServicer_to_server,
        port=50051))