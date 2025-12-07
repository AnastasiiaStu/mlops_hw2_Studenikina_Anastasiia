import os
import sys
import pickle
import grpc
import numpy as np
from concurrent import futures

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from generated import model_pb2, model_pb2_grpc

class PredictionServicer(model_pb2_grpc.PredictionServiceServicer):
    def __init__(self):
        model_path = os.getenv('MODEL_PATH', 'models/model.pkl')
        self.version = os.getenv('MODEL_VERSION', 'v1.0.0')
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
        print(f"Model loaded: {model_path}")

    def Health(self, request, context):
        return model_pb2.HealthResponse(
            status="ok",
            model_version=self.version
        )

    def Predict(self, request, context):
        if not request.features:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Empty features')
            return model_pb2.PredictResponse()
        
        features = np.array(request.features).reshape(1, -1)
        pred = self.model.predict(features)[0]
        proba = self.model.predict_proba(features)[0]
        conf = float(proba[pred])
        
        return model_pb2.PredictResponse(
            prediction=str(pred),
            confidence=conf,
            model_version=self.version
        )

def serve():
    port = os.getenv('PORT', '50051')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    model_pb2_grpc.add_PredictionServiceServicer_to_server(
        PredictionServicer(), server
    )
    server.add_insecure_port(f'[::]:{port}')
    print(f"Server started on port {port}")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()