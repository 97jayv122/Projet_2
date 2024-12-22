import os
import csv
import re
import requests
from models import BASE_URL, BASE_URL_CATEGORY,en_tete ,DOSSIER, Category
from view import View
import sys

class Controller:
    def __init__(self, category, view):
        self.category = category
        self.view = view

    def make_directory(self, folder):
        """Vérifie si le dossier existe ou le crée."""
        if not os.path.exists(folder):
            os.makedirs(folder)

    def folder_rename(self, folder_name):
        """ Pour chaque url des catégories appliquent le chargement de l'en tête en
            lui attribuant le nom passé en argumant catégorie ou titre.

        Args:
            folder_name str: catégorie de livre 

        Returns:
        str: Chemin d'accès du fichier CSV
        """
        return "books_datas/" + folder_name + ".csv"

    def clean_title(self, name):
        """ Retire les caractères spéciaux qui bloque le renommage du fichier

        Args:
            name (str): titre du livre brut de l'affichage du site

        Returns:
        str: titre nettoyé des caractères spéciaux et raccourcis.
        """
        return re.sub(r'[\\/*?:"<>|’“”]', "", name)[:100]
    def load(self, file_name, data):
        """Ecris sur le fichier csv les données. 

        Args:
            file_name (str): Nom du dossier avec le chemin d'accès au fichier
            data (liste): données d'un livre
        """
        with open(file_name, "a", newline="", encoding="utf-8") as fichier_csv:
            writer = csv.writer(fichier_csv, delimiter=";")
            writer.writerow(data)
    
    def save_image(self, title_clean, folder, image_url):
        """ Fonction enregistrant l'image du livre

        Args:
            title_clean (str): est le nom du livre 
            folder (str): chemin du dossier d'enregistrement
            image_url (str): lien url de l'image à enregistrer
        """
        # Etablit un chemin cible de dossier en fonction de la catégorie
        dossier_image = "images/"+ folder + "/"
        # Vérifie l'existence du chemin du dossier sinon le crée
        self.make_directory(dossier_image)
        # Création de chemin d'accèes avec le nom de l'image
        name_file = "images/"+ folder + "/" + title_clean + ".jpg"
        # Télécharge et enregistre l'image du livre dans le dossier de sa catégorie
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(name_file, "wb") as picture_file:
                picture_file.write(response.content)

    def run(self):
        # Vérifie si des arguments sont passés à l'èxécution et éxécute le script par défaut
        if len(sys.argv) < 2:
            self.view.prompt_extract_all_categories()
            # Vérifie l'existence du chemin du dossier sinon le crée.
            self.make_directory(DOSSIER)
            # appelle la fonction pour extrait les urls des catégories et les noms des catégories
            url_from_categories = self.category.extract_categories(BASE_URL)
            for url_from_category, name in url_from_categories.items():
                file_csv_name = self.folder_rename(name)
                self.load(file_csv_name, en_tete)
                # Pour chaque url des catégories, récupère les urls de chaque livre de la catégorie et si il
                # y' a plusieurs pages les parcours.
                url_books_from_category = self.category.url_book_category_page(url_from_category)
                # Parcours la liste des liens de page de livre.
                for book_url in url_books_from_category:
                    # Chaque lien de page livre est chargé dans la fonction extrayant les données du livre.
                    datas = self.category.extract(book_url)
                    title = self.clean_title(datas[2])
                    self.save_image(title, datas[7], datas[9])
                    self.load(file_csv_name, datas)
            self.view.prompt_extract_finish()
            self.view.prompt_location_datas()
            self.view.prompt_location_images()
        else :
            # Premier argument définit l'action extraire une catégorie (category) ou un livre (book).
            action = sys.argv[1]

            match action:

                case "category":
                    try:
                        url = sys.argv[2]

                    except IndexError:

                        self.view.prompt_enter_url_category()
                        #  Sortie avec érreur.
                        sys.exit(1)

                    if "index.html" in url:

                        url = url.replace("/index.html","")

                    self.make_directory(DOSSIER)
                    # permet d'extraire le nom de la catégorie via l'url et la transformer tel que récuperé
                    # dans la page d'un livre pour charger l'en-tête.
                    category_name = url.replace(BASE_URL+"catalogue/category/books/","").strip("/").rstrip("_")
                    category_name = category_name.split("_")[0]
                    category_name = category_name.capitalize()
                    file_csv_name = self.folder_rename(category_name)
                    self.load(file_csv_name, en_tete)
                    url_books_from_category = self.category.url_book_category_page(url)
                    for book_url in url_books_from_category:

                        datas = self.category.extract(book_url)
                        title = self.clean_title(datas[2])
                        self.save_image(title, datas[7], datas[9])
                        self.load(file_csv_name, datas)

                    self.view.prompt_location_datas_category(category_name)
                    self.view.prompt_location_images_category(category_name)

                case "book":

                    try:
                        url = sys.argv[2]

                    except IndexError:

                        self.view.prompt_enter_url_book()
                        #  Sortie avec érreur.
                        sys.exit(1)

                    self.make_directory(DOSSIER)
                    datas = self.category.extract(url)
                    title_book = self.clean_title(datas[2])
                    file_csv_name = self.folder_rename(title_book)
                    self.load(file_csv_name, en_tete)
                    self.load(file_csv_name, datas)
                    self.save_image(title_book, title_book, datas[9])
                    self.view.prompt_location_datas_book(title_book)
                    self.view.prompt_location_image_book(title_book)

                case _:

                    self.view.prompt_invalid_action(action)