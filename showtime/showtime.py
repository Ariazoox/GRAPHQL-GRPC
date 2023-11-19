import grpc
from concurrent import futures
import showtime_pb2
import showtime_pb2_grpc
import json

class ShowtimeServicer(showtime_pb2_grpc.ShowtimeServicer):

    def __init__(self):
        with open('{}/data/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]

    def GetShwotime(self, request, context):
        return showtime_pb2.ShowtimeList(schedule=self.db)

        return showtime_pb2.ScheduleData(date='', movies=[])

    def Get_movie_by_date(self, request, conext):
        for booking in self.db:
            if booking['date'] == request.date:
                return showtime_pb2.ScheduleData(date=booking['date'], movies=booking['movies'])

        return showtime_pb2.ScheduleData(date='', movies=[])



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    showtime_pb2_grpc.add_ShowtimeServicer_to_server(ShowtimeServicer(), server)
    server.add_insecure_port('[::]:3000')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
