# has all controller logic (the while loop and stuff will go here)
# also will convert image url to bytes
from model_pipelines.proto import ControllerService_pb2, ControllerService_pb2_grpc
from model_pipelines.proto import ModelService_pb2, ModelService_pb2_grpc
import grpc
import requests
import time
import threading

class ControllerService(ControllerService_pb2_grpc.ControllerServiceServicer):
    def __init__(self):
        self.stubs = {
            "detect":ModelService_pb2_grpc.ModelServiceStub(grpc.insecure_channel('localhost:50052')),
            "enhance":ModelService_pb2_grpc.ModelServiceStub(grpc.insecure_channel('localhost:50053'))
        }
        self._lock = threading.Lock()
        self._active_requests = 0


    def ProcessPipeline(self, request, context):
        # the request in this case would be an image_url and an order?
        with self._lock:
            self._active_requests += 1

        try:
            print("Received request:", request)
            image_bytes = requests.get(request.image_url).content
            pipeline = request.pipeline_steps

            for model in pipeline:
                if model not in self.stubs:
                    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
                    context.set_details('Model not implemented!')
                    raise NotImplementedError('Model not implemented!')
                start_time = time.perf_counter()
                image_bytes = self.model_out(model, image_bytes)
                end_time = time.perf_counter()
                latency = (end_time - start_time)
                print(f"[{model}] latency: {latency:.4f}s")
                print(f"active requests: {self.get_active_request_count()}")

            return ControllerService_pb2.PipelineOutput(final_image=image_bytes)

        finally:
            with self._lock:
                self._active_requests -= 1

    def model_out(self, model_name: str, image_bytes):
        stub = self.stubs[model_name]
        response = stub.Predict(ModelService_pb2.ImageRequest(image_data=image_bytes))
        return response.result_image

    def get_active_request_count(self):
        with self._lock:
            return self._active_requests



