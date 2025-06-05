import asyncio
import aiohttp
import time
from grpc import aio
import grpc
from model_pipelines.servers.server_runner import run_grpc_server
from model_pipelines.detect import DetectService
from model_pipelines.enhance import EnhanceService
from model_pipelines.proto import ControllerService_pb2, ControllerService_pb2_grpc
from model_pipelines.proto import ModelService_pb2, ModelService_pb2_grpc
from model_pipelines.proto.ModelService_pb2_grpc import add_ModelServiceServicer_to_server, ModelServiceStub

class ControllerService(ControllerService_pb2_grpc.ControllerServiceServicer):
    def __init__(self):
        self.stubs = {
            "detect0": ModelServiceStub(aio.insecure_channel('localhost:50052')),
            "enhance0": ModelServiceStub(aio.insecure_channel('localhost:50053')),
        }
        self._lock = asyncio.Lock()
        self._active_requests = 0
        self.detect_ports = [50052]
        self.enhance_ports = [50053]
        self.stub_index = {"detect": 0, "enhance": 0}
        self.last_scale_time = {"detect": 0, "enhance": 0}
        self.max_replicas = {"detect": 3, "enhance": 2}
        self.shutdown_events = []
        self.server_tasks = []

    async def ProcessPipeline(self, request, context):
        async with self._lock:
            self._active_requests += 1

        try:
            print("Received request:", request)
            async with aiohttp.ClientSession() as session:
                async with session.get(request.image_url) as resp:
                    image_bytes = await resp.read()

            pipeline = request.pipeline_steps

            for model in pipeline:
                if model not in ["detect", "enhance"]:
                    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
                    context.set_details("Model not implemented!")
                    raise NotImplementedError("Model not implemented!")

                if (
                    self.get_active_request_count() > 10
                    and self.should_scale(model)
                    and self.can_scale(model)
                ):
                    if model == "detect":
                        await self.scale_up_detect()
                    elif model == "enhance":
                        await self.scale_up_enhance()

                start_time = time.perf_counter()
                image_bytes = await self.model_out(model, image_bytes)
                end_time = time.perf_counter()
                latency = end_time - start_time
                print(f"[{model}] latency: {latency:.4f}s")
                print(f"active requests: {self.get_active_request_count()}")

            return ControllerService_pb2.PipelineOutput(final_image=image_bytes)

        finally:
            async with self._lock:
                self._active_requests -= 1

    async def model_out(self, model_name: str, image_bytes):
        async with self._lock:
            if model_name == "detect":
                stub_key = f"detect{self.stub_index[model_name] % len(self.detect_ports)}"
            else:
                stub_key = f"enhance{self.stub_index[model_name] % len(self.enhance_ports)}"
            self.stub_index[model_name] += 1
            print(f"Routing {model_name} request to {stub_key}")

        stub = self.stubs[stub_key]
        response = await stub.Predict(ModelService_pb2.ImageRequest(image_data=image_bytes))
        return response.result_image

    def get_active_request_count(self):
        return self._active_requests

    async def scale_up_detect(self):
        new_port = self.detect_ports[-1] + 2
        self.detect_ports.append(new_port)
        event = asyncio.Event()
        self.shutdown_events.append(event)
        task = asyncio.create_task(run_grpc_server(
            servicer_cls=DetectService,
            add_servicer_fn=add_ModelServiceServicer_to_server,
            port=new_port,
            shutdown_event=event
        ))
        self.server_tasks.append(task)
        self.stubs[f"detect{new_port - self.detect_ports[0]}"] = ModelServiceStub(
            aio.insecure_channel(f"localhost:{new_port}")
        )
        self.last_scale_time["detect"] = time.perf_counter()

    async def scale_up_enhance(self):
        new_port = self.enhance_ports[-1] + 2
        self.enhance_ports.append(new_port)
        event = asyncio.Event()
        self.shutdown_events.append(event)
        task = asyncio.create_task(run_grpc_server(
            servicer_cls=EnhanceService,
            add_servicer_fn=add_ModelServiceServicer_to_server,
            port=new_port,
            shutdown_event=event
        ))
        self.server_tasks.append(task)
        self.stubs[f"enhance{new_port - self.enhance_ports[0]}"] = ModelServiceStub(
            aio.insecure_channel(f"localhost:{new_port}")
        )
        self.last_scale_time["enhance"] = time.perf_counter()

    def should_scale(self, model):
        return time.perf_counter() - self.last_scale_time[model] > 10

    def can_scale(self, model):
        if model == "detect":
            return len(self.detect_ports) < self.max_replicas["detect"]
        elif model == "enhance":
            return len(self.enhance_ports) < self.max_replicas["enhance"]
        else:
            raise ValueError(f"Unknown model: {model}")

    async def shutdown(self):
        for event in self.shutdown_events:
            event.set()  # trigger each run_grpc_server shutdown
        for task in self.server_tasks:
            try:
                await task
            except asyncio.CancelledError:
                print("⚠️ Server task cancelled during shutdown.")
        print("✅ All scale-out servers shut down.")
