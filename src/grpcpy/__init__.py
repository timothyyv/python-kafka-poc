import grpc
from concurrent import futures
from aggregator_functions import Aggregator
import requests
import time
import json
import aiohttp
import grpcpy.server.aggregations_pb2_grpc as pb2_grpc
import grpcpy.server.aggregations_pb2 as pb2


class AggregationService(pb2_grpc.AggregationServicer):

    def __init__(self, *args, **kwargs):
        self.aggregator = Aggregator()
        pass

    def SendAggregation(self, request, context):
        # async with aiohttp.ClientSession() as session:
        parsedMsg = json.loads(request.input)
        # check condition to redirect method
        if parsedMsg['action'] == "sum":
            response = self.aggregator.sum(parsedMsg)
        elif parsedMsg['action'] == "sum_if":
            response = self.aggregator.sum_if(parsedMsg)
        elif parsedMsg['action'] == "count":
            response = self.aggregator.count(parsedMsg)
        elif parsedMsg['action'] == "count_if":
           response = self.aggregator.count_if(parsedMsg)

        # response = self.aggregator.s

        # print("Status:", response.status_code)
        # print("Content-type:", response.headers['content-type'])

        # html = response.json()
        print(response, "HERE")
        return pb2.AggregationResponse(value=response)
        # print("Body:", html[:15], "...")

        # print(f'Message incoming: {request.name}')
        


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_AggregationServicer_to_server(AggregationService(), server)
    server.add_insecure_port('[::]:9090')
    server.start()
    server.wait_for_termination()