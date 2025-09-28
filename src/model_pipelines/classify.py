import torch
import PIL
import torchvision.transforms as transforms
import warnings
warnings.filterwarnings('ignore')
import io
from model_pipelines.proto import ModelService_pb2_grpc, ModelService_pb2

class ClassifyService(ModelService_pb2_grpc.ModelServiceServicer):
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f'Using {self.device} for inference')
        self.efficientnet = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_efficientnet_b0', pretrained=True)
        self.utils = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_convnets_processing_utils')
        self.efficientnet.eval().to(self.device)

        print("✅ ClassifyService ready.")


    async def Predict(self, request, context):
        image = request.image_data
        image = PIL.Image.open(io.BytesIO(image))

        #preprocess image
        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

        pil_images = [
            image
        ]

        batch = torch.stack([preprocess(img) for img in pil_images]).to(self.device)

        with torch.no_grad():
            output = torch.nn.functional.softmax(self.efficientnet(batch), dim=1)
        results = self.utils.pick_n_best(predictions=output, n=5)

        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        for result in results:
            print(result)
        final_bytes = buffer.getvalue()

        return ModelService_pb2.ImageResponse(result_image=final_bytes)