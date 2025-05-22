# has all controller logic (the while loop and stuff will go here)
# also will convert image url to bytes

from model_pipelines.proto import ControllerService_pb2, ControllerService_pb2_grpc
from model_pipelines.proto import ModelService_pb2, ModelService_pb2_grpc
import grpc
import requests


class ControllerService(ControllerService_pb2_grpc.ControllerServiceServicer):
    def __init__(self):
        self.stubs = {
            "detect":ModelService_pb2_grpc.ModelServiceStub(grpc.insecure_channel('localhost:50051')),
            "enhance":ModelService_pb2_grpc.ModelServiceStub(grpc.insecure_channel('localhost:50052'))
        }

    def ProcessPipeline(self, request, context):
        # the request in this case would be an image_url and an order?
        print("Received request:", request)

        image_bytes = requests.get(request.image_url).content
        pipeline = request.pipeline_steps

        for model in pipeline:
            if model not in self.stubs:
                context.set_code(grpc.StatusCode.UNIMPLEMENTED)
                context.set_details('Model not implemented!')
                raise NotImplementedError('Model not implemented!')
            image_bytes = self.model_out(model, image_bytes)

        return ControllerService_pb2.PipelineOutput(final_image=image_bytes)


    def model_out(self, model_name, image_bytes):
        stub = self.stubs[model_name]
        response = stub.Predict(ModelService_pb2.ImageRequest(image_data=image_bytes))
        return response.result_image


