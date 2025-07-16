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
  - you will need to download grafana, k6, influxdbv2
  - there might be some compatibility issues with influxdbv2 and grafana scraping, but there is an official k6 extension that supports this
```
influxdb # to start the influxdb
# follow a guide elsewhere to see how to get started using influx
# will be at http://localhost:8086
```
```
brew services start grafana # starts the grafana server
# you will once again need to login, so follow a guide elsehwere
# will be at http://localhost:3000
```
- then run the following to test your script.js k6 script
```
K6_INFLUXDB_ORGANIZATION="<INFLUXDB-ORGANIZATION-NAME>" \
K6_INFLUXDB_BUCKET="<INFLUXDB-BUCKET-NAME>" \
K6_INFLUXDB_TOKEN="<INFLUXDB-TOKEN>" \
K6_INFLUXDB_ADDR="<INFLUXDB-HTTP-ADDRESS>" \
./k6 run <name_of_your_test>.js -o xk6-influxdb
```
---
- to run grafana dashboards and get realtime data with k6 + influxdb, run these commands in your terminal (windows powershell)
  - you will need to download grafana, k6, influxdbv1 (IMPORTANT THAT IT IS V1)

```
# FOR GRAFANA
# example paths
# logins are same as on macOS

C:\Program Files\GrafanaLabs\grafana\bin> .\grafana-server.exe

# follow guide to setup Grafana on windows
# will be at http://localhost:3000
```

```
# FOR INFLUXDB
# example paths
# logins are same as on macOS (hopefully)

C:\Program Files\InfluxData\influxdb> .\influxd.exe

# follow guide to setup InfluxDB v1 (!!!) 
# will be at http://localhost:8086
# dont be worried if link displays "404 page not found" - this is how it's meant to be (i think)
```

```
# the last thing to run in the terminal is the testing k6 script
k6 run --out influxdb=http://localhost:8086/k6 ./tests/<name_of_your_test>.js
```