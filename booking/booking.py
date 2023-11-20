import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import json
import showtime_pb2_grpc
import showtime_pb2


class BookingServicer(booking_pb2_grpc.BookingServicer):

    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]

    # Fonction qui récupère les réservations d'un utilisateur
    def GetUserBookings(self, request, context):
        # Boucle qui parcourt nos bookings
        for booking in self.db:
            # Vérification de l'existence de l'ID dans le fichier bookings.json
            if request.userid == booking["userid"]:
                return booking_pb2.BookingData(
                    userid=booking["userid"], dates=booking["dates"])

    # Fonction qui ajoute une réservation pour un utilisateur en faisant appel à Showtime pour la vérification
    def AddBookingByUser(self, request, context):
        schedule = []
        with grpc.insecure_channel("localhost:3000") as channel:
            stub = showtime_pb2_grpc.ShowtimeStub(channel)
            schedule = stub.GetShowtime(showtime_pb2.Empty()).schedule
        # Boucle qui parcourt nos schedules
        for schedule_item in schedule:
            # On vérifie la correspondance des dates/movieid
            if (
                    schedule_item.date == request.date
                    and request.movieid in schedule_item.movies
            ):
                # Boucle qui parcourt les données de bookings.json
                for booking in self.db:
                    # Vérification de l'ID
                    if booking["userid"] == request.userid:
                        # Boucle pour parcourir les dates dans bookings.json
                        for item in booking["dates"]:
                            # Vérification des dates
                            if item["date"] == request.date:
                                # On vérifie si le movie id est inexistant, si c'est le cas, on l'ajoute
                                if request.movieid not in item["movies"]:
                                    item["movies"].append(request.movieid)
                                else:
                                    return
                            else:
                                booking["dates"].append(
                                    {
                                        "date": request.date,
                                        "movies": [request.movieid],
                                    }
                                )
                        return booking_pb2.BookingData(
                            userid=booking["userid"], dates=booking["dates"]
                        )
                # On considère cette fois le user id valide
                self.db.append(
                    {
                        "userid": request.userid,
                        "dates": [{"date": request.date, "movies": [request.movieid]}],
                    }
                )
                return booking_pb2.BookingData(
                    userid=self.db[-1]["userid"], dates=self.db[-1]["dates"]
                )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port('[::]:3002')
    server.start()
    print("Server started")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
