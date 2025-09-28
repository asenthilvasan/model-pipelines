import grpc from 'k6/net/grpc';
import { check } from 'k6';

const client = new grpc.Client();
client.load(['../src/model_pipelines/proto'], 'ControllerService.proto');

export const options = {
  scenarios: {
    peaky: {
      executor: 'ramping-arrival-rate',
      startRate: 1,           // starting RPS
      timeUnit: '1s',
      preAllocatedVUs: 1500,
      maxVUs: 1500,
      gracefulStop: '0s',
      stages: [
        { duration: '15s', target: 50 }, // ramp from 1 → 50
        { duration: '15s', target: 20 }, // ramp 50 → 20
        { duration: '15s', target: 80 }, // ramp 20 → 80
        { duration: '15s', target: 70 }, // ramp 80 → 70
        { duration: '15s', target: 80 }, // ramp 70 → 80
        { duration: '15s', target: 30 }, // ramp 80 → 30
        { duration: '15s', target: 20 }, // ramp 30 → 20
      ],
    },
  },
};

export default () => {
  client.connect('localhost:50051', { plaintext: true });

  const data = {
    //image_url: "https://ultralytics.com/images/zidane.jpg",
    image_url: "https://raw.githubusercontent.com/ai-forever/Real-ESRGAN/refs/heads/main/inputs/lr_image.png",
    pipeline_steps: ["detect", "classify"]
  };

  const res = client.invoke('ControllerService/ProcessPipeline', data);

  if (!check(res, {
    'status is OK': (r) => r && r.status === grpc.StatusOK,
  })) {
    console.error(`❌ Failed with status: ${res && res.status}`);
  }

  client.close();
};