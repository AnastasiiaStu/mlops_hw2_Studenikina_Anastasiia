import os
import sys
import grpc

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from generated import model_pb2, model_pb2_grpc

def make_stub(addr="localhost:50051"):
    channel = grpc.insecure_channel(addr)
    return model_pb2_grpc.PredictionServiceStub(channel)

def health(stub):
    res = stub.Health(model_pb2.HealthRequest(), timeout=5.0)
    print(f"Health: {res.status}, version: {res.model_version}")

def predict(stub, features, label=""):
    req = model_pb2.PredictRequest(features=features)
    res = stub.Predict(req, timeout=5.0)
    print(f"Predict{' ' + label if label else ''}: class={res.prediction}, confidence={res.confidence:.4f}, version={res.model_version}")

def main():
    addr = os.getenv('GRPC_SERVER', 'localhost:50051')
    print(f"Connecting to {addr}")
    
    stub = make_stub(addr)
    
    health(stub)
    predict(stub, [5.1, 3.5, 1.4, 0.2], "(Setosa)")
    predict(stub, [6.7, 3.1, 4.7, 1.5], "(Versicolor)")
    predict(stub, [7.2, 3.0, 5.8, 1.6], "(Virginica)")

if __name__ == '__main__':
    main()