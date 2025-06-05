import torch
from PIL import Image
from RealESRGAN import RealESRGAN
import io
from model_pipelines.proto import ModelService_pb2_grpc, ModelService_pb2
# load models and define model logic here

class EnhanceService(ModelService_pb2_grpc.ModelServiceServicer):
    def __init__(self):
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        self.model = RealESRGAN(device, scale=4)
        self.model.load_weights('weights/RealESRGAN_x4.pth', download=True)
        print("✅ EnhanceService ready.")

    async def Predict(self, request, context):
        image = request.image_data
        image = Image.open(io.BytesIO(image))
        sr_image = self.model.predict(image)

        buffer = io.BytesIO()
        sr_image.save(buffer, format="JPEG")

        final_bytes = buffer.getvalue()

        return ModelService_pb2.ImageResponse(result_image=final_bytes)