## Clustering de Livres à partir d'une Base de Données d'Amazon
##### AGIER Olivier - CHEVALIER Arnaud

L'objectif de ce projet est de réaliser une opération de clustering sur les données brutes présentes dans une base de données du site Amazon.com . L'idée est de regrouper ces livres dans un certains nombre de clusters cohérents (livres d'un même auteur, titres similaires...), afin de pouvoir y appliquer différents algorithmes dans le cadre d'un projet d'option.

A partir des données brutes de départ, on cherche à créer une connaissance de similarité entre les livres. Ce n'est cependant pas un système de recommandation. On ne cherche pas à trier les livres par pertinence par rappport à un ou plusieurs autres, mais bien à découper les `837188` éléments du set de base en un certain nombre de clusters.

L'ensemble du code et de la documentation du porjet se trouve dans le fichier `clustering.ipynb`.

Le set de données de base est `amazon_livres.txt`.
Le set de test est `test_set.csv`.

Il y a aussi deux dossiers : `pre_processing` et `scoring`, ils comportent des fonctions utiles au traitement des données et au calul de performance. 
