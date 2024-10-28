# Projet_2 (etl)

## Description

Script permettant de parcourir les catégories du site [https://books.toscrape.com](https://books.toscrape.com). 
Le script extrait les informations des livres par catégorie, les enregistre dans des fichiers CSV dans le dossier `book_datas`, 
et télécharge les images des livres dans le dossier `images`, classées par catégorie.

## Fonctionnalités

- Parcours des catégories de livres sur le site.
- Extraction des informations des livres, telles que :
  - URL de la page produit.
  - Code universel du produit (UPC).
  - Titre du livre.
  - Prix TTC et HT.
  - Disponibilité.
  - Description.
  - Catégorie.
  - Note de l'avis.
  - URL de l'image.
- Téléchargement les images dans des dossiers organisés par catégorie.

## Prérequis

- Python 3.7+
- `requests` : pour envoyer des requêtes HTTP.
- `beautifulsoup4` : pour analyser le contenu HTML.

## Installation

1. Clonez le dépôt :

   git clone https://github.com/97jayv122/Projet_2.git
   cd main.py

2. Installer les dépendances :
   
   pip install -r requirements.txt

3. Exécution du script :

   python main.py

## Sortie
  Les fichiers CSV sont enregistrés dans le dossier book_datas avec les informations des livres pour chaque catégorie.
  Les images sont téléchargées dans des sous-dossiers du dossier images, organisées par catégorie.

