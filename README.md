# Model Pipelines

    * Author: Ashwin Senthilvasan
    * Date: May 2025

trying to simulate ml model pipelines locally using gRPC and PyTorch

 - part of machine learning pipeline research @ UCSC with faculty in Baskin Engineering

## Setup Notes
 - REAL-ESRGAN.models will need to be changed slightly 
 - if CUDA is enabled (you have a GPU), you need to run this command after installing other dependencies with poetry

```poetry run pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121```
 
 - you can check if CUDA is properly working by doing

```
import torch

print(torch.cuda.is_available()) # -> should print True if installed correctly
```

- to run the ghz load tests, navigate to tests/ghz-windows-x86_64 in the terminal and run this command (Windows powershell)

```
.\ghz.exe --proto ../../src/model_pipelines/proto/ControllerService.proto `
  --call ControllerService/ProcessPipeline `
  -D payload.json `
  -c 10 -n 100 `
  --insecure `
  localhost:50053
```