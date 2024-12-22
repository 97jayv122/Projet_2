import requests
from bs4 import BeautifulSoup
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

class Category:
    def __init__(self):
        pass

    def sibling_url(self, url):
        """ Récupère l'objet BeautifulSoup de l'url

        Args:
            url (str): liens pages web à analyser

        Returns: 
            objet BeautifulSoup représentant la structure HTML de la page
        """
        response = requests.get(url)
        if response.status_code == 200:
            page = response.content
            soup = BeautifulSoup(page, "html.parser")
            return soup
        else:
            print(f"Erreur lors de la récupération de la page : {response.status_code}")
            return None

    def extract_categories(self, url):
        """Extrait l' url de chaque catégories et le nom de la catégorie dans deux listes distincte 
        puis fusionné dans un dictionnaire url_categories.

        Args:
            url_main (str): url de la page d'accueil du site books to scrape

        Returns:
            liste: liste contenant les liens url des catégories.
        """
        soup = self.sibling_url(url)
        categories = soup.find("ul", class_="nav nav-list").find_all("a")[1:]
        url_categories = {}
        urls = []
        names = []
        for category in categories:
            urls.append(BASE_URL + "/".join(category["href"].split("/")[:-1]))
            names.append(category.string.strip())
        url_categories.update({url: name for url, name in zip(urls, names)})
        return url_categories
    
    def url_book_category_page(self, url_category):
        """Fonction renvoyant toutes les urls des livres d'une catégorie dans une liste,
        si il y'a plusieurs pages les parcours.L a fonction prend en argument le l'url
        d'une catégorie de livre. 

        Args:
            url_category (str): lien url d'une catégorie

        Returns:
            liste: liste contenant les urls des livres d'une catégorie.
        """
        url_books_of_category = []
        url_pages_books = []
        soup = self.sibling_url(url_category)
        # Cherche la balise indiquant la page actuelle et le nombre de page totale de cette catégorie
        nombres_page = soup.find("li", class_="current")
        if nombres_page:
            for i in range(1, (int(nombres_page.string.split()[3])+1)):
                url_pages_category = url_category + "/page-" + str(i) + ".html"
                url_pages_books.append(self.sibling_url(url_pages_category)
                                       .find("ol", class_="row").find_all("a", title=True))
            for url_page_books in url_pages_books:
                for url_page_book in url_page_books:
                    url_books_of_category.append(BASE_URL_CATEGORY + url_page_book["href"].strip("./"))
        else:
            url_pages_books.append(soup.find("ol", class_="row").find_all("a", title=True))
            for url_page_books in url_pages_books:
                for url_page_book in url_page_books:
                    url_books_of_category.append(BASE_URL_CATEGORY + url_page_book["href"].strip("./"))
        return url_books_of_category
    
    def rating_number(self, rating_stars):
        """ Retourne la valeur de la clé de rating_stars qui est une chaîne de caractère,
        qui est un nombre entier"""
        rating_list = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
        if rating_stars.capitalize() in rating_list:
            return rating_list[rating_stars]
        
    def extract(self, book):
        """Fonction avec en argument l'url d'un livre qui va extraire les infos d'un livre et ajouter
        à la liste datas et télécharger l'image du livre dans le dossier de sa catégorie situé dans
        le dossier images.

        Args:
            book (str): lien url de la page d'un livre

        Returns:
            liste: liste contenant les informations du livre.
        """
        datas = []
        soup = self.sibling_url(book)
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
            # Remplace les virgules et les points virgules par un
            # espaces pour éviter les érreurs sur le fichier csv
            description = description.string.replace(","," ")
            description_clean = description.replace(";"," ")
            datas.append(description_clean)
        else:
            datas.append("")
        # Ajoute la catégorie du livre à la liste datas
        category = soup.find("ul").find_all("li")[2].find("a").string
        datas.append(category)
        # Ajoute le review rating en chiffre à la liste datas
        rating_stars = soup.find("p" ,class_="star-rating").get("class")[1]
        review_rating = self.rating_number(rating_stars)
        datas.append(review_rating)
        # Ajoute l'url complet de l'image.
        image_url = soup.find("div", class_="carousel-inner").find("img")["src"].strip("./")
        image_url = BASE_URL + image_url
        datas.append(image_url)
        return datas