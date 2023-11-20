Réalisations dans le TP API mixtes GRAPHQL-GRPC:

- On conserve les même sevices que dans le TP REST, à savoir : Movie, Booking, Times et User mais avec des quelques API cette fois ci écrites en GraphQL et en gRPC.

- Réecriture du service Movie en GraphQL.

- Modification du service user qui fait maintenant des requêtes GraphQL et non plus REST.

- Création des fichiers d'API proto pour les services Times et Booking.

- Ecriture des codes des service Booking et Showtime avec les fonctions définies dans nos fichiers proto.

- Dans le service GRPC Booking, on définit des appels de procédures distantes vers Showtime en utilisant les stub associés, Booking devient alors un serveur et un client GRPC.

- Dans le service REST User, on définit des appels de procédures distantes vers Booking en utilisant les stub associés, User devient alors un client gRPC et reste un serveur REST.

Instructions pour pouvoir lancer le code:

- Installer PyCharm (version 2023.1.3 de préfèrence).
- Installer Postman.
- Télécharger le contenu du repository git suivant: https://github.com/Ariazoox/GRAPHQL-GRPC.git
- Extraire le dossier "GRAPHQL-GRPC" dans votre bureau ou dans n'importe quel dossier.
- Lancer PyCharm, séléctionner "Open" puis ouvrez le dossier "GRAPHQL-GRPC".
- Vous aurez un message automatique de PyCharm pour installer un intérprète Python, cliquez sur "Install".
- Vous aurez ensuite un autre message pour installer les requirements donc encore une fois, cliquez sur "Install" (sinon vous ouvrez le "Terminal" en bas puis vous collez la commande suivante: pip install -r requirements.txt.
- Vous pourrez ensuite lancer chaque service en appuyant sur "Run" en haut à droite.
