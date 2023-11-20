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
