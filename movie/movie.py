from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, ObjectType, QueryType, MutationType
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify, make_response

import resolvers as r

PORT = 3001
HOST = '0.0.0.0'
app = Flask(__name__)

# Chargement du schéma GraphQL depuis un fichier externe
type_defs = load_schema_from_path('movie.graphql')

# Création des objets GraphQL
query = QueryType()
movie = ObjectType('Movie')
query.set_field('movie_with_id', r.movie_with_id)
mutation = MutationType()
mutation.set_field('update_movie_rate', r.update_movie_rate)
actor = ObjectType('Actor')
movie.set_field('actors', r.resolve_actors_in_movie)

# Création du schéma exécutable
schema = make_executable_schema(type_defs, movie, query, mutation, actor)

# Point d'entrée renvoyant à la page d'accueil "Welcome to the Movie service!"
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>", 200)

# Redirige vers le Playground GraphQL.
@app.route('/graphql', methods=['GET'])
def playground():
    return PLAYGROUND_HTML, 200

# Permet de tester des requêtes GraphQL
@app.route('/graphql', methods=['POST'])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=None,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

if __name__ == "__main__":
    print("Server running on port %s"%(PORT))
    app.run(host=HOST, port=PORT)
