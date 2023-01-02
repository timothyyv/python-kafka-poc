# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import grpcpy.server.aggregations_pb2 as aggregations__pb2


class AggregationStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SendAggregation = channel.unary_unary(
                '/aggregation.Aggregation/SendAggregation',
                request_serializer=aggregations__pb2.AggregationRequest.SerializeToString,
                response_deserializer=aggregations__pb2.AggregationResponse.FromString,
                )


class AggregationServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SendAggregation(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AggregationServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SendAggregation': grpc.unary_unary_rpc_method_handler(
                    servicer.SendAggregation,
                    request_deserializer=aggregations__pb2.AggregationRequest.FromString,
                    response_serializer=aggregations__pb2.AggregationResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'aggregation.Aggregation', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Aggregation(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SendAggregation(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/aggregation.Aggregation/SendAggregation',
            aggregations__pb2.AggregationRequest.SerializeToString,
            aggregations__pb2.AggregationResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
