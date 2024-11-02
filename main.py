#!/usr/bin/python
#-*-coding: utf-8-*-
"""
Script pour parcourir les catégories du site https://books.toscrape.com/,
extraire les informations des livres par catégorie dans un fichier CSV dans un dossier
datas et télécharge les images des livres dans le dossier catégorie 
qui est associer dans un dossier images.
"""
import sys
from fonctions import *
BASE_URL = "https://books.toscrape.com/"
BASE_URL_CATEGORY = BASE_URL+"catalogue/"
DOSSIER = "books_datas"
en_tete = [
    "product_page_url",
    "universal_product_code",
    "title",
    "price_TT(£)", 
    "price_HT(£)",
    "number_available",
    "product_description",
    "category",
    "review_rating",
    "image_url"]

if __name__ == "__main__" :
    # Vérifie si des arguments sont passés à l'èxécution et éxécute le script par défaut
    if len(sys.argv) < 2:
        print("l'extraction des données pour chaque catégorie du site books to scrape est en cours.")
        # Vérifie l'existence du chemin du dossier sinon le crée.
        directory(DOSSIER)
        # appelle la fonction pour extrait les urls des catégories et les noms des catégories
        url_from_categories = extract_categories(BASE_URL)
        for url_from_category, name in url_from_categories.items():
            file_csv_name = folder_rename(name)
            load(file_csv_name, en_tete)
            # Pour chaque url des catégories, récupère les urls de chaque livre de la catégorie et si il
            # y' a plusieurs pages les parcours.
            url_books_from_category = url_book_category_page(url_from_category)
            # Parcours la liste des liens de page de livre.
            for book_url in url_books_from_category:
                # Chaque lien de page livre est chargé dans la fonction extrayant les données du livre.
                datas = extract(book_url)
                title = clean_title(datas[2])
                save_image(title, datas[7], datas[9])
                load(file_csv_name, datas)
        print("Extraction réussite !!")
        print("Écriture des données dans un fichier csv au nom de la catégorie dans le dossier book_datas")
        print("Enregistrement des images dans le sous-dossier d' images aux noms de leur catégorie")
    else :
        # Premier argument définit l'action extraire une catégorie (category) ou un livre (book).
        action = sys.argv[1]

        match action:

            case "category":
                try:
                    url = sys.argv[2]

                except IndexError:

                    print("Vous devez fournir l'url de la catégorie.")
                    #  Sortie avec érreur.
                    sys.exit(1)

                if "index.html" in url:

                    url = url.replace("/index.html","")

                directory(DOSSIER)
                # permet d'extraire le nom de la catégorie via l'url et la transformer tel que récuperé
                # dans la page d'un livre pour charger l'en-tête.
                category_name = url.replace(BASE_URL+"catalogue/category/books/","").strip("/").rstrip("_")
                category_name = category_name.split("_")[0]
                category_name = category_name.capitalize()
                file_csv_name = folder_rename(category_name)
                load(file_csv_name, en_tete)
                url_books_from_category = url_book_category_page(url)
                for book_url in url_books_from_category:

                    datas = extract(book_url)
                    title = clean_title(datas[2])
                    save_image(title, datas[7], datas[9])
                    load(file_csv_name, datas)

                print(f"Données de la catégorie {category_name} extraite dans le dossier book_datas.")
                print(f"Images de la catégorie {category_name} enregistrez dans le dossier images.")

            case "book":

                try:
                    url = sys.argv[2]

                except IndexError:

                    print("Vous devez fournir l'url de la catégorie.")
                    #  Sortie avec érreur.
                    sys.exit(1)

                directory(DOSSIER)
                datas = extract(url)
                title_book = clean_title(datas[2])
                file_csv_name = folder_rename(title_book)
                load(file_csv_name, en_tete)
                load(file_csv_name, datas)
                save_image(title_book, title_book, datas[9])
                print(f"Données du livre: {title_book} extrait dans book_datas.")
                print(f"Image du livre: {title_book} enregistré dans le dossier images.")

            case _:

                print(f"Action inconnue : {action}. utilisez category ou book")