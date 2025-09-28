import torch
import os
from PIL import Image
import io
from model_pipelines.proto import ModelService_pb2_grpc, ModelService_pb2
import numpy as np
# load models and define model logic here

class DetectService(ModelService_pb2_grpc.ModelServiceServicer):
    def __init__(self):

        # Force YOLOv5 to skip CUDA device detection internally
        os.environ["CUDA_VISIBLE_DEVICES"] = "0" if torch.cuda.is_available() else ""

        # Load YOLOv5 model
        # possible models: https://github.com/ultralytics/yolov5#pretrained-checkpoints
        # possible_models goes from light models (key 1) to heavy models (key 5) and repeated for other 4 ending in "6"
        possible_models = {
            1: "yolov5n",
            2: "yolov5s",
            3: "yolov5m",
            4: "yolov5l",
            5: "yolov5x",
            6: "yolov5n6",
            7: "yolov5s6",
            8: "yolov5m6",
            9: "yolov5l6",
        }
        self.model = torch.hub.load("ultralytics/yolov5", possible_models[1], force_reload=False)

        # Move it to the proper device manually
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        # print(self.model) # can double check GPU / CPU use here

    async def Predict(self, request, context):
        image = request.image_data
        input_image = Image.open(io.BytesIO(image))
        sr_image = self.model(input_image)
        image = Image.fromarray(sr_image.render()[0].astype(np.uint8))

        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")

        final_bytes = buffer.getvalue()

        return ModelService_pb2.ImageResponse(result_image=final_bytes)