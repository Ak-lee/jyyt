# service.py
import time
import grpc
import predict_pb2 as pb2
import predict_pb2_grpc as pb2_grpc
from concurrent import futures
from 单辆列车年里程增长预测 import predict_generate

class Service(pb2_grpc.PredictServicer):
    def predict(self, request, context):
        trainId = request.trainId
        deadline = request.deadline

        predict_generate(trainId, deadline)
        code = 765
        return pb2.Result(code=code)

def run():
    grpc_server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=4),
    )
    pb2_grpc.add_PredictServicer_to_server(Service(), grpc_server)
    grpc_server.add_insecure_port('0.0.0.0:5000')
    print('server start..')
    grpc_server.start()

    try:
        while 1:
            time.sleep(3600)
    except KeyboardInterrupt:
        grpc_server.stop(0)

if __name__ == '__main__':
    run()