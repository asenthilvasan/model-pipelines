import grpc from 'k6/net/grpc';
import { check } from 'k6';

const client = new grpc.Client();
client.load(['../src/model_pipelines/proto'], 'ControllerService.proto');

export const options = {
  scenarios: {
    step1: {
      executor: 'constant-arrival-rate',
      rate: 1,
      timeUnit: '1s',
      duration: '15s',
      preAllocatedVUs: 1500,
      maxVUs: 1500,
      startTime: '0s',
      gracefulStop: '0s',
    },
    step2: {
      executor: 'constant-arrival-rate',
      rate: 50,
      timeUnit: '1s',
      duration: '15s',
      preAllocatedVUs: 1500,
      maxVUs: 1500,
      startTime: '15s',
      gracefulStop: '0s',
    },
    step3: {
      executor: 'constant-arrival-rate',
      rate: 20,
      timeUnit: '1s',
      duration: '15s',
      preAllocatedVUs: 1500,
      maxVUs: 1500,
      startTime: '30s',
      gracefulStop: '0s',
    },
    step4: {
      executor: 'constant-arrival-rate',
      rate: 80,
      timeUnit: '1s',
      duration: '15s',
      preAllocatedVUs: 1500,
      maxVUs: 1500,
      startTime: '45s',
      gracefulStop: '0s',
    },
    step5: {
      executor: 'constant-arrival-rate',
      rate: 70,
      timeUnit: '1s',
      duration: '15s',
      preAllocatedVUs: 1500,
      maxVUs: 1500,
      startTime: '60s',
      gracefulStop: '0s',
    },
    step6: {
      executor: 'constant-arrival-rate',
      rate: 80,
      timeUnit: '1s',
      duration: '15s',
      preAllocatedVUs: 1500,
      maxVUs: 1500,
      startTime: '75s',
      gracefulStop: '0s',
    },
    step7: {
      executor: 'constant-arrival-rate',
      rate: 30,
      timeUnit: '1s',
      duration: '15s',
      preAllocatedVUs: 1500,
      maxVUs: 1500,
      startTime: '90s',
      gracefulStop: '0s',
    },
    step8: {
      executor: 'constant-arrival-rate',
      rate: 20,
      timeUnit: '1s',
      duration: '15s',
      preAllocatedVUs: 1500,
      maxVUs: 1500,
      startTime: '105s',
      gracefulStop: '0s',
    },
  },
};

export default () => {
  client.connect('localhost:50051', { plaintext: true });

  const res = client.invoke('ControllerService/ProcessPipeline', {
    image_url:
      'https://raw.githubusercontent.com/ai-forever/Real-ESRGAN/refs/heads/main/inputs/lr_image.png',
    pipeline_steps: ['detect'],
  });

  check(res, { 'status is OK': (r) => r && r.status === grpc.StatusOK });

  client.close();
};