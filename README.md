# RoyalRideRentals

- Introduction à PyQt6
PyQt6 est une bibliothèque de développement d'interface utilisateur pour Python basée sur Qt, le framework d'interface utilisateur multiplateforme bien connu. PyQt6 fournit une grande variété de widgets et de fonctionnalités pour créer des applications graphiques avancées. Il est également livré avec des outils pour créer des interfaces utilisateur riches en graphiques, telles que des graphiques, des tableaux et des visualisations de données.

- Description du projet :
Le projet consiste en une application de location de voitures de luxe. L'application permet aux utilisateurs de réserver une voiture de leur choix pour une durée de location spécifique. Les utilisateurs peuvent également effectuer des paiements via l'application pour confirmer leur réservation. L'application dispose d'une interface pour les utilisateurs et d'une interface pour les administrateurs.

- Côté utilisateur :
L'interface utilisateur permet aux utilisateurs de visualiser les voitures disponibles et de les filtrer en fonction de leurs préférences. Ils peuvent également effectuer une recherche pour trouver une voiture spécifique. Une fois qu'ils ont sélectionné une voiture, ils peuvent entrer les dates de location et effectuer un paiement pour finaliser la réservation. S'ils n'ont pas de compte, ils peuvent créer un compte et stocker les informations de compte dans une table de base de données MySQL.

- Côté administrateur :
L'interface administrateur permet aux administrateurs de visualiser toutes les réservations en cours et passées. Ils peuvent également ajouter, modifier ou supprimer des voitures de la liste des voitures disponibles. Les administrateurs ont également visualisr la liste des voitures.

- Interface welcome.ui :
L'interface welcome.ui est la première interface utilisateur que les utilisateurs voient lorsqu'ils lancent l'application. Cette interface permet aux utilisateurs de se connecter à leur compte s'ils en ont un. S'ils n'ont pas de compte, ils peuvent cliquer sur un bouton pour créer un nouveau compte. Les informations de compte nouvellement créées seront stockées dans une table de base de données MySQL.
Les utilisateurs disposant d'un compte d'administrateur peuvent également se connecter à leur interface d'administration personnalisée en utilisant un nom d'utilisateur et un mot de passe personnalisés. Cette interface d'administration leur permettra de gérer les voitures de luxe disponibles à la location, de visualiser les réservations passées et en cours.

En outre, il y a des icônes pour chaque plateforme de réseaux sociaux que j'utilise (par exemple, LinkedIn, Discord etc.) sur cette interface pour permettre aux utilisateurs d'interagir avec moi en dehors de l'application.

- Interface Accueil1 :
L'interface Accueil1 est l'interface principale pour les utilisateurs normaux connectés. Cette interface leur permet de visualiser toutes les voitures de luxe disponibles à la location, de réserver une ou plusieurs voitures en choisissant le nombre de jours et la date de début et de fin de la location. Ils peuvent également afficher toutes leurs réservations passées et en cours, ainsi que suivre l'état de leur réservation en temps réel.

En plus de cela, l'interface Accueil1 peut inclure des fonctionnalités supplémentaires telles que la recherche de voitures par marque, modèle, année ou type de carburant. Les utilisateurs peuvent également trier les voitures par prix ou disponibilité, afin de trouver rapidement la voiture qui correspond le mieux à leurs besoins.

Cette interface peut également inclure des informations supplémentaires sur chaque voiture, telles que des photos, des descriptions détaillées, des spécifications techniques. Cela aidera les utilisateurs à prendre une décision éclairée avant de réserver une voiture.
- Interface register.ui : 
L'interface Register.ui permet aux nouveaux utilisateurs de créer un compte sur la plateforme. Pour s'inscrire, les utilisateurs doivent fournir les informations suivantes :
--Nom d'utilisateur
--Prénom
--Nom de famille
--Adresse e-mail
--Sexe
Toutes ces informations seront stockées dans la base de données pour permettre aux utilisateurs de se connecter à leur compte ultérieurement.
Lorsqu'un utilisateur s'inscrit, la plateforme doit vérifier si le nom d'utilisateur est déjà utilisé par un autre utilisateur. Si c'est le cas, la plateforme doit signaler à l'utilisateur que ces informations sont déjà prises et l'inviter à fournir des informations différentes.
Enfin, une fois que l'utilisateur s'est inscrit avec succès, l'interface Register.ui va rediriger l'utilisateur vers la page d'accueil de la plateforme, où il pourra voir toutes les voitures disponibles à la location et commencer à réserver une voiture.

- Interface Acceuil2 : 
L'interface Acceuil.ui est réservée à l'administrateur de la plateforme de location de voitures de luxe. L'administrateur peut accéder à cette interface en se connectant avec son nom d'utilisateur et son mot de passe personnels.

Une fois connecté, l'administrateur peut visualiser toutes les voitures disponibles à la location, ainsi que toutes les réservations en cours. L'administrateur peut ajouter, modifier ou supprimer des voitures de la base de données en utilisant des boutons dédiés. Les informations concernant chaque voiture, telles que le modèle, l'année de fabrication, le prix et le type de carburant, peuvent être mises à jour par l'administrateur.

L'administrateur peut également visualiser toutes les réservations actuelles. Pour chaque réservation, l'administrateur peut voir les informations relatives à la voiture louée, la date de début de la location, ainsi que les coordonnées du client qui a effectué la réservation. L'administrateur peut approuver ou rejeter chaque réservation en utilisant des boutons dédiés.
