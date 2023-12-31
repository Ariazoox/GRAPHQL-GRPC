# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import showtime_pb2 as showtime__pb2


class ShowtimeStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetShowtime = channel.unary_unary(
                '/Showtime/GetShowtime',
                request_serializer=showtime__pb2.Empty.SerializeToString,
                response_deserializer=showtime__pb2.ShowtimeList.FromString,
                )


class ShowtimeServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetShowtime(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ShowtimeServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetShowtime': grpc.unary_unary_rpc_method_handler(
                    servicer.GetShowtime,
                    request_deserializer=showtime__pb2.Empty.FromString,
                    response_serializer=showtime__pb2.ShowtimeList.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Showtime', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Showtime(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetShowtime(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Showtime/GetShowtime',
            showtime__pb2.Empty.SerializeToString,
            showtime__pb2.ShowtimeList.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
