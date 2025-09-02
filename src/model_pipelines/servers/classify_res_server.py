# server logic
from model_pipelines.classify_res import ClassifyResnetService
from model_pipelines.proto.ModelService_pb2_grpc import add_ModelServiceServicer_to_server, ModelServiceServicer
import asyncio
from model_pipelines.servers.server_runner import run_grpc_server

if __name__ == '__main__':
    asyncio.run(run_grpc_server(
        servicer_cls=ClassifyResnetService,
        add_servicer_fn=add_ModelServiceServicer_to_server,
        port=50055))