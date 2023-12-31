Réalisations dans le TP API mixtes GRAPHQL-GRPC:

On conserve les mêmes services que dans le TP REST, à savoir : Movie, Booking, Times et User, mais avec quelques API cette fois-ci écrites en GraphQL et en gRPC.

Réécriture du service Movie en GraphQL.

Modification du service User qui fait maintenant des requêtes GraphQL et non plus REST.

Création des fichiers d'API proto pour les services Times et Booking.

Écriture des codes des services Booking et Showtime avec les fonctions définies dans nos fichiers proto.

Dans le service gRPC Booking, on définit des appels de procédures distantes vers Showtime en utilisant les stubs associés. Booking devient alors un serveur et un client gRPC.

Dans le service REST User, on définit des appels de procédures distantes vers Booking en utilisant les stubs associés. User devient alors un client gRPC et reste un serveur REST.

Instructions pour pouvoir lancer le code:

Installer PyCharm (version 2023.1.3 de préférence).
Installer Postman.
Télécharger le contenu du dépôt git suivant : https://github.com/Ariazoox/GRAPHQL-GRPC.git
Extraire le dossier "GRAPHQL-GRPC" sur votre bureau ou dans n'importe quel dossier.
Lancer PyCharm, sélectionner "Open" puis ouvrez le dossier "GRAPHQL-GRPC".
Vous aurez un message automatique de PyCharm pour installer un interprète Python, cliquez sur "Install".
Vous aurez ensuite un autre message pour installer les requirements, donc encore une fois, cliquez sur "Install" (sinon, ouvrez le "Terminal" en bas, puis collez la commande suivante : pip install -r requirements.txt).
Vous pourrez ensuite lancer chaque service en appuyant sur "Run" en haut à droite.
ChatGPT
Pour exécuter les requêtes, le principe est le même que dans le TP FLASK-REST, à l'exception des requêtes GRPC pour lesquelles il est nécessaire d'importer les fichiers protos avant de pouvoir invoquer les fonctions.
