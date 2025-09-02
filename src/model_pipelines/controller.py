import asyncio
import grpc
import aiohttp
from grpc import aio
from model_pipelines.proto import ControllerService_pb2, ControllerService_pb2_grpc
from model_pipelines.proto import ModelService_pb2, ModelService_pb2_grpc

class ControllerService(ControllerService_pb2_grpc.ControllerServiceServicer):
    def __init__(self):
        self.stubs = {
            "detect": ModelService_pb2_grpc.ModelServiceStub(aio.insecure_channel('localhost:50052')),
            "enhance": ModelService_pb2_grpc.ModelServiceStub(aio.insecure_channel('localhost:50053')),
            "classify": ModelService_pb2_grpc.ModelServiceStub(aio.insecure_channel('localhost:50054')),
            "classify_res": ModelService_pb2_grpc.ModelServiceStub(aio.insecure_channel('localhost:50055')),
        }
        self._lock = asyncio.Lock()
        self._active_requests = 0

    async def ProcessPipeline(self, request, context):
        async with self._lock:
            self._active_requests += 1

        try:
            print("Received request:", request)

            # Asynchronously fetch image bytes
            async with aiohttp.ClientSession() as session:
                async with session.get(request.image_url) as resp:
                    image_bytes = await resp.read()

            pipeline = request.pipeline_steps

            for model in pipeline:
                if model not in self.stubs:
                    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
                    context.set_details('Model not implemented!')
                    raise NotImplementedError('Model not implemented!')

                start_time = asyncio.get_event_loop().time()
                image_bytes = await self.model_out(model, image_bytes)
                end_time = asyncio.get_event_loop().time()
                latency = end_time - start_time
                print(f"[{model}] latency: {latency:.4f}s")
                print(f"active requests: {self.get_active_request_count()}")

            return ControllerService_pb2.PipelineOutput(final_image=image_bytes)

        finally:
            async with self._lock:
                self._active_requests -= 1

    async def model_out(self, model_name: str, image_bytes):
        stub = self.stubs[model_name]
        response = await stub.Predict(ModelService_pb2.ImageRequest(image_data=image_bytes))
        return response.result_image

    def get_active_request_count(self):
        return self._active_requests
