import re
import os
import csv
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
BASE_URL_CATEGORY = BASE_URL+"catalogue/"
DOSSIER = "book_datas"

def sibling_url(url):
    """Fonction envoyant une requête HTTP à une url pour récupéré la page html avec requests,
    vérifie que la requête aboutie avec une valeur de status code qui doit être a [200]. 
    Ainsi nous poouvons Analyser la page html récupéré et l'a transormez
    en un objet BeautifulSoup que nous retournons

    Args:
        url (str): liens pages web à analyser

    Returns:
       BeautifulSoup: objet BeautifulSoup représentant la structure HTML de la page
    """
    response = requests.get(url)
    if response.status_code == 200:
        page = response.content
        soup = BeautifulSoup(page, "html.parser")
        return soup
    else:
        print(f"Erreur lors de la récupération de la page : {response.status_code}")
        return None

def folder_rename(folder_name):
    """ Pour chaque url des catégories appliquent le chargement de l'en tête en
        lui attribuant le nom de la catégorie.

    Args:
        folder_name str: catégorie de livre 

    Returns:
       str: Chemin d'accès du fichier CSV
    """
    return "book_datas/" + folder_name + ".csv"

def directory(folder):
    """Vérifie si le dossier existe ou le créer."""
    if not os.path.exists(folder):
        os.makedirs(folder)

def save_image(image_name, folder, image_url):
    # Etablit un chemin cible de dossier en fonction de la catégorie
    dossier_image = "images/"+ folder + "/"
    # Vérifie l'existence du chemin du dossier sinon le crée
    directory(dossier_image)
    # Retire les caractères spéciaux pouvant bloquer l'écriture du nom du fichier
    # et limite le nombre de caractère
    title_clean = re.sub(r'[\\/*?:"<>|]', "", image_name)[:255]
    name_file = "images/"+ folder + "/" + title_clean + ".jpg"
    # Télécharge et enregistre l'image du livre dans le dossier de sa catégori
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(name_file, "wb") as picture_file:
            picture_file.write(response.content)

def extract(book):
    """Fonction avec en argument l'url d'un livre qui va extraire les infos d'un livre et ajouter
    à la liste datas et télécharger l'image du livre dans le dossier de sa catégorie situé dans
    le dossier images."""
    datas = []
    soup = sibling_url(book)
    if soup is None:
        print(f"Impossible de récupérer le contenu pour {book}.")
        return []
    # Ajoute l'url de la page du livre à la liste datas.
    datas.append(book)
    # Ajoute l'UPC du livre à la liste datas.
    universal_product_code = soup.find("table", class_="table table-striped").find("td").string
    datas.append(universal_product_code)
    # Ajoute le titre du livre à liste datas.
    title = soup.h1.string
    datas.append(title)
    # Ajoute le prix incluant la taxe.
    price_including_tax = soup.find("table", class_="table table-striped").find_all("td")[2].string
    datas.append(price_including_tax.strip("£"))
    # Ajoute le prix hors taxe.
    price_excluding_tax = soup.find("table", class_="table table-striped").find_all("td")[3].string
    datas.append(price_excluding_tax.strip("£"))
    # Ajoute le nombre de livre disponible à la liste datas.
    availability = soup.find("table", class_="table table-striped").find_all("td")[5].string
    number_available = ''.join(filter(str.isdigit, availability.split()[2]))
    datas.append(number_available)
    # Vérifie la présence d'une description et Ajoute la description du livre à la liste datas.
    description = soup.find("p", class_=None)
    if description :
        datas.append(description.string)
    else:
        datas.append("")
    # Ajoute la catégorie du livre à la liste datas
    category = soup.find("ul").find_all("li")[2].find("a").string
    datas.append(category)
    # Ajoute le review rating en chiffre à la liste datas
    rating_stars = soup.find("p" ,class_="star-rating").get("class")[1]
    review_rating = rating_number(rating_stars)
    datas.append(review_rating)
    # Ajoute l'url complet de l'image.
    image_url = soup.find("div", class_="carousel-inner").find("img")["src"].strip("./")
    image_url = BASE_URL + image_url
    datas.append(image_url)
    save_image(title, category, image_url)
    return datas, category

def rating_number(rating_stars):
    """ Retourne la valeur de la clé de rating_stars qui est une chaîne de caractère,
    qui est un nombre entier"""
    rating_list = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    if rating_stars.capitalize() in rating_list:
        return rating_list[rating_stars]

def load(file_name, data):
    """ Ecris sur le fichier csv les données. """
    with open(file_name, "a", newline="", encoding="utf-8") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=';',quoting=csv.QUOTE_MINIMAL)
        writer.writerow(data)

def url_book_category_page(url_category):
    """ Fonction renvoyant toutes les urls des livres d'une catégorie dans une liste,
    si il y'a plusieurs pages les parcours.L a fonction prend en argument le l'url
    d'une catégorie de livre. """
    url_books_of_category = []
    url_pages_books = []
    soup = sibling_url(url_category)
    # Cherche la balise indiquant la page actuelle et le nombre de page totale de cette catégorie
    nombres_page = soup.find("li", class_="current")
    if nombres_page:
        for i in range(1, (int(nombres_page.string.split()[3])+1)):
            url_pages_category = url_category + "/page-" + str(i) + ".html"
            url_pages_books.append(sibling_url(url_pages_category).find("ol", class_="row").find_all("a", title=True))
        for url_page_books in url_pages_books:
            for url_page_book in url_page_books:
                url_books_of_category.append(BASE_URL_CATEGORY + url_page_book["href"].strip("./"))
    else:
        url_pages_books.append(soup.find("ol", class_="row").find_all("a", title=True))
        for url_page_books in url_pages_books:
            for url_page_book in url_page_books:
                url_books_of_category.append(BASE_URL_CATEGORY + url_page_book["href"].strip("./"))
    return url_books_of_category

def extract_categories(url_main):
    """ Extrait l' url de chaque catégories et le nom de la catégorie dans deux listes distincte 
    puis fusionné dans un dictionnaire url_categories."""
    soup = sibling_url(url_main)
    categories = soup.find("ul", class_="nav nav-list").find_all("a")[1:]
    url_categories = {}
    urls = []
    names = []
    for category in categories:
        urls.append(BASE_URL + "/".join(category["href"].split("/")[:-1]))
        names.append(category.string.strip())
    url_categories.update({url: name for url, name in zip(urls, names)})
    return url_categories