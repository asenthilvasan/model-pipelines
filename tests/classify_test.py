import torch
import PIL
import torchvision.transforms as transforms
import numpy as np
import json
import requests
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
print(f'Using {device} for inference')
# efficientnet models go from b0 to b7 with FLOPS of 0.39B to 37B
efficientnet = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_efficientnet_b0', pretrained=True)
utils = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_convnets_processing_utils')

efficientnet.eval().to(device)

uris = [
    'https://raw.githubusercontent.com/ai-forever/Real-ESRGAN/refs/heads/main/inputs/lr_image.png',
    'http://images.cocodataset.org/test-stuff2017/000000028117.jpg',
    'http://images.cocodataset.org/test-stuff2017/000000006149.jpg',
    'http://images.cocodataset.org/test-stuff2017/000000004954.jpg',
]

batch = torch.cat(
    [utils.prepare_input_from_uri(uri) for uri in uris]
).to(device)

with torch.no_grad():
    output = torch.nn.functional.softmax(efficientnet(batch), dim=1)

results = utils.pick_n_best(predictions=output, n=5)

for uri, result in zip(uris, results):
    img = PIL.Image.open(requests.get(uri, stream=True).raw)
    img.thumbnail((256,256), PIL.Image.Resampling.LANCZOS)
    plt.imshow(img)
    plt.show()
    print(result)