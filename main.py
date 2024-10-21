import csv
import requests
from bs4 import BeautifulSoup

datas =[]
base_url = "https://books.toscrape.com/"
base_url_category = "https://books.toscrape.com/catalogue/"
url_books_in_category = []
url_pages_livres = []
category =""
# Fonction renvoyant un soup en fonctioin de l'url donné
def sibling_url(url):
    response = requests.get(url)
    page = response.content
    return BeautifulSoup(page, "html.parser")
# Fonction extrayant les données du livre
def extraire(url_books_in_category):
    global base_url
    global datas
    global category
    datas = []
    category 
    soup = sibling_url((url_books_in_category))
    # Ajoute l'url de la page du livre à la lliste datas
    data_load(url_books_in_category)
    # Ajoute l'UPC du livre à la liste datas
    universal_product_code = soup.find("table", class_="table table-striped").find("td").string
    data_load(universal_product_code)
    # Ajoute le titre du livre à liste datas
    title = soup.h1.string
    data_load(title)
    # Ajoute le prix incluant la taxe
    price_including_tax = soup.find("table", class_="table table-striped").find_all("td")[2].string
    data_load(price_including_tax)
    # Ajoute le prix hors taxe
    price_excluding_tax = soup.find("table", class_="table table-striped").find_all("td")[3].string
    data_load(price_excluding_tax)
    # Ajoute le nombre de livre disponible à la liste
    availability = soup.find("table", class_="table table-striped").find_all("td")[5].string
    number_available = ''.join(filter(str.isdigit, availability.split()[2]))
    data_load(number_available)
    # Ajoute la description du livre à la liste datas
    description = soup.find("p", class_=None)
    if description : 
        data_load(description.string)
    else:
        
        data_load("")
    # Ajoute la catégorie du livre à la liste datas
    category = soup.find("ul").find_all("li")[2].find("a").string
    data_load(category)
    # Ajoute le review rating en chiffre à la liste datas
    evaluation_avis = soup.find("p" ,class_="star-rating").get("class")[1]
    review_rating = rating_number(evaluation_avis)
    data_load(review_rating)
    # Ajoute l'url complet de l'image 
    image_url = soup.find("div", class_="carousel-inner").find("img")["src"].strip("./")
    image_url = base_url + image_url
    data_load(image_url)
    return category

# Fonctions chargeant une donné dans une liste
def data_load(data):
    global datas
    datas.append(data)

# fonction permettant de récupéré un nombre a partir du dictionnaire en se servant de la variable evaluation_avis
def rating_number(evaluation_avis):
    rating_list = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    if evaluation_avis.capitalize() in rating_list:
        return rating_list[evaluation_avis]
# Ecris sur le fichiers csv les données  
def charger(datas):
    with open("data.csv", "a", newline="", encoding="utf-8") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        writer.writerow(datas)
        
# def etl(url_book_in_category):   
# Fonction extrayant l'url de chaque catégorie dans une liste
def extractions_categories(url_main):
    soup = sibling_url(url_main)
    categories = soup.find("ul", class_="nav nav-list").find_all("a")[1:]
    url_categories = [base_url + "/".join(category["href"].split("/")[:-1]) for category in categories]
    return url_categories

# Fonction renvoyant tout les urls des livres d'une catégorie dans une liste
def url_book_category_page(url_category):
    global base_url_category
    global url_books_in_category
    global url_pages_livres
    soup = sibling_url(url_category)
    if soup.find("li", class_="current"):
        for i in range(2, (int(soup.find("li", class_="current").string.split()[3])+1)):
            url_pages_category = url_category + "/page-" + str(i) + ".html"
            url_pages_livres.append(sibling_url(url_pages_category).find("ol", class_="row").find_all("a", title=True))
        for url_page_livres in url_pages_livres:
            for url_page_livre in url_page_livres:
                url_books_in_category.append(base_url_category + url_page_livre["href"].strip("./"))
    else:
        url_pages_livres.append(soup.find("ol", class_="row").find_all("a", title=True))        
        for url_page_livres in url_pages_livres:
            for url_page_livre in url_page_livres:
                url_books_in_category.append(base_url_category + url_page_livre["href"].strip("./"))
    
    return url_books_in_category

if __name__ == "__main__" : 
    en_tete = [
    "product_page_url",
    "universal_product_code", 
    "title", 
    "price_including_tax", 
    "price_excluding_tax",
    "number_available",
    "product_description",
    "category",
    "review_rating",
    "image_url"]
    charger(en_tete)
    url_categories = extractions_categories(base_url)
    
    for url_category in url_categories:
        url_books_in_category = url_book_category_page(url_category)
        print(url_books_in_category)
        
        for url_book_in_category in url_books_in_category:
            print(url_book_in_category)
            
            extraire(url_book_in_category)

            charger(datas)
        
        datas = []
            
            # etl(url_book_in_category) 


    
