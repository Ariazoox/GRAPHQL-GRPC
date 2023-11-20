# REST API
from flask import Flask, render_template, request, jsonify, make_response
import requests
import json

from movie.resolvers import movie_with_id
from werkzeug.exceptions import NotFound

# CALLING gRPC requests
import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc

# CALLING GraphQL requests


app = Flask(__name__)

PORT = 3203
HOST = 'localhost'

with open('{}/data/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]
   print(users)


# Point d'entrée qui renvoie à la page d'accueil "Welcome to the User service!"
@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"


# Point d'entrée pour afficher un utilisateur selon son ID
@app.route("/users/<userid>", methods=['GET'])
def get_user_by_id(userid):
    # Boucle parcourant nos users
    for user in users:
        # Vérification de la correspondance des ID
        if str(user["id"]) == str(userid):
            res = make_response(jsonify(user), 200)
            return res
    # Message d'erreur au cas où l'ID serait inexistant
    return make_response(jsonify({"error": "User ID not found"}), 400)

# Point d'accès qui affiche, pour un utilisateur donné, ses réservations.
@app.route("/users/<userid>/bookings", methods=["GET"])
def get_user_bookings(userid):
    bookings = []
    returned_booking = {}
    # Appel au service booking
    with grpc.insecure_channel("localhost:3002") as channel:
        stub = booking_pb2_grpc.BookingStub(channel)
        booking = stub.GetUserBookings(booking_pb2.UserId(userid=userid))

        returned_booking["userid"] = booking.userid
        returned_booking["dates"] = []

    for date_item in booking.dates:
        mapped_movies = []
        for movie_id in date_item.movies:
            # Requête GRAPHQL qui remplace la requête REST
            query = """
                {
                    movie_with_id (_id: "%s"){
                        title,
                        id,
                        rating,
                        director
                    }
                }
            """ % (
                movie_id
            )
            # Appel du service movie
            res = requests.post(url="http://localhost:3001/graphql", json={"query": query})
            movie = res.json()
            mapped_movies.append(movie["data"]["movie_with_id"])

        returned_booking["dates"].append(
            {"date": date_item.date, "movies": mapped_movies}
        )

    return make_response(jsonify(returned_booking), 200)

# Ajoute un booking pour un utilisateur selon son ID donné en paramètre
@app.route("/users/<userid>/bookings", methods=["POST"])
def book_for_user(userid):
    data = request.get_json()
    
    # Appel du service booking 
    with grpc.insecure_channel("localhost:3002") as channel:
        
        stub = booking_pb2_grpc.BookingStub(channel)
        # Appel de la fonction AddBookingByUser du service booking
        try:
            stub.AddBookingByUser(
                booking_pb2.BookingPayload(
                    userid=userid, date=data["date"], movieid=data["movieid"]
                )
            )
            return make_response(jsonify({"message": "Booking added successfully"}))
        # Message d'erreur si la vérification échoue
        except Exception as e:
            print(e)
            return make_response(
                jsonify(
                    {
                        "error": "The date or the movieid is not correct, make sure the date is in the showtime table, that the movie is part of it, and that it's not already reserved."
                    }
                ),
                400,
            )

if __name__ == "__main__":
   print("Server running on port %s"%(PORT))
   app.run(host=HOST, port=PORT)
