import torch
import PIL
import torchvision.transforms as transforms
import warnings
warnings.filterwarnings('ignore')
import io
from model_pipelines.proto import ModelService_pb2_grpc, ModelService_pb2

class ClassifyResnetService(ModelService_pb2_grpc.ModelServiceServicer):
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f'Using {self.device} for inference')
        self.resnet = torch.hub.load('pytorch/vision:v0.10.0', 'resnet18', pretrained=True)
        self.resnet.eval().to(self.device)

        print("✅ Classify(ResNet) Service ready.")


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

        input_tensor = preprocess(image)
        input_batch = input_tensor.unsqueeze(0)
        input_batch = input_batch.to(self.device, non_blocking=True)

        with torch.no_grad():
            output = self.resnet(input_batch)

        probabilities = torch.nn.functional.softmax(output[0], dim=0)

        with open("imagenet_classes.txt", "r") as f:
            categories = [s.strip() for s in f.readlines()]
        # Show top categories per image
        top5_prob, top5_catid = torch.topk(probabilities, 5)

        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        for i in range(top5_prob.size(0)):
            print(categories[top5_catid[i]], top5_prob[i].item())
        print("\n")
        final_bytes = buffer.getvalue()

        return ModelService_pb2.ImageResponse(result_image=final_bytes)