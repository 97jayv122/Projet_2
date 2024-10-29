# Projet_2 (etl)

## Description

Ce script Python permet de parcourir les catégories du site [https://books.toscrape.com](https://books.toscrape.com), d'extraire les informations des livres par catégorie et de les enregistrer dans des fichiers CSV. Il télécharge également les images des livres dans des dossiers organisés par catégorie.

## Fonctionnalités

- Parcours des catégories de livres sur le site et extraction des informations par catégorie.
- Extraction des informations pour un livre spécifique à partir de son URL.
- Enregistrement des informations des livres dans des fichiers CSV avec les colonnes suivantes :
  - URL de la page produit.
  - Code universel du produit (UPC).
  - Titre du livre.
  - Prix TTC et HT.
  - Disponibilité.
  - Description.
  - Catégorie.
  - Note (rating).
  - URL de l'image.
- Téléchargement des images des livres et organisation dans des sous-dossiers par catégorie.

## Prérequis

- Python 3.10+
- `requests` : pour envoyer des requêtes HTTP.
- `beautifulsoup4` : pour analyser le contenu HTML.

## Installation

1. Clonez le dépôt :
   `bash`
   
   `git clone https://github.com/97jayv122/Projet_2.git`
   `cd Projet_2`

2. Installer les dépendances :
   
   `pip install -r requirements.txt`

## Utilisation
### 1. Extraction de toutes les catégories.
   
   Si vous ne fournissez aucun argument, le script extraira les informations de toutes les catégories et les enregistrera dans des fichiers CSV,
   tout en téléchargeant les images dans des sous-dossiers rangé par catégorie dans le dossier images.:

   `python main.py`

### 2. Extraction d'une catégorie spécifique.
   Pour extraire les informations d'une catégorie particulière, utilisez la commande suivante :

   `python main.py category https://books.toscrape.com/catalogue/category/books/science_22/`

#### 3. Extraction d'un livre spécifique.
   Pour extraire les informations d'un livre en particulier, utilisez la commande suivante :

   `python main.py book https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html`

## Structure des dossiers de sortie.

Les fichiers CSV sont enregistrés dans le dossier book_datas (créé automatiquement) avec les informations des livres pour chaque catégorie.
Les images sont téléchargées dans des sous-dossiers du dossier images, organisées par catégorie.

## Exemple de sortie.

Après l'exécution du script pour une catégorie, vous trouverez :

Un fichier CSV nommé science.csv dans le dossier book_datas contenant toutes les informations des livres de cette catégorie.
Les images des livres dans le dossier images/science/, avec le titre des livres comme nom de fichier.

## Auteurs
97jay122
