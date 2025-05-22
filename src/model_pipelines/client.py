# client stuff - opens stubs, etc.
import grpc
from model_pipelines.proto import ControllerService_pb2_grpc, ControllerService_pb2
from PIL import Image
from io import BytesIO
import time

def main():
    channel = grpc.insecure_channel("localhost:50053")

    stub = ControllerService_pb2_grpc.ControllerServiceStub(channel)

    request = ControllerService_pb2.PipelineRequest(
            image_url="https://raw.githubusercontent.com/ai-forever/Real-ESRGAN/main/inputs/lr_lion.png",
            pipeline_steps=["detect"]
        )

    response = stub.ProcessPipeline(request)

    image = Image.open(BytesIO(response.final_image))
    image.show()

if __name__ == "__main__":
    main()