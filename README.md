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
  localhost:50051
```

- to run grafana dashboards and get realtime data with k6 + influxdb, run these commands in your terminal (macOS)
  - you will need to download grafana, k6, influxdb
```
influxdb # to start the influxdb
# follow a guide elsewhere to see how to get started using influx
```
```
brew services start grafana # starts the grafana server
# you will once again need to login, so follow a guide elsehwere
```
- then run the following to test your script.js k6 script
```
K6_INFLUXDB_ORGANIZATION="<INFLUXDB-ORGANIZATION-NAME>" \
K6_INFLUXDB_BUCKET="<INFLUXDB-BUCKET-NAME>" \
K6_INFLUXDB_TOKEN="<INFLUXDB-TOKEN>" \
K6_INFLUXDB_ADDR="<INFLUXDB-HTTP-ADDRESS>" \
./k6 run script.js -o xk6-influxdb
```
