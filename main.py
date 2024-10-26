import re
import csv
import requests
from bs4 import BeautifulSoup


base_url = "https://books.toscrape.com/"
base_url_category = base_url+"catalogue/"
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

def sibling_url(url):
    """Fonction envoyant une requête à une url passée en argument à la fonction avec requests, vérifie que la requête aboutie 
    avec une valeur de status code qui doit être a [200]. Ainsi nous poouvons Analyser la page html récupéré et l'a transormez 
    en un objet BeautifulSoup que nous allons retourner """
    response = requests.get(url)
    if response.status_code == 200:
        page = response.content
    else:
        print(f"Erreur lors de la récupération de la page : {response.status_code}")
   
    return BeautifulSoup(page, "html.parser")

def extract(book_url):
    """ Fonction avec en argument l'url d'un livre qui vas intégrer à la liste datas """
    datas = []
    soup = sibling_url(book_url)
    # Ajoute l'url de la page du livre à la lliste datas
    datas.append(book_url)
    # Ajoute l'UPC du livre à la liste datas
    universal_product_code = soup.find("table", class_="table table-striped").find("td").string
    datas.append(universal_product_code)
    # Ajoute le titre du livre à liste datas
    title = soup.h1.string
    datas.append(title)
    # Ajoute le prix incluant la taxe
    price_including_tax = soup.find("table", class_="table table-striped").find_all("td")[2].string
    datas.append(price_including_tax)
    # Ajoute le prix hors taxe
    price_excluding_tax = soup.find("table", class_="table table-striped").find_all("td")[3].string
    datas.append(price_excluding_tax)
    # Ajoute le nombre de livre disponible à la liste
    availability = soup.find("table", class_="table table-striped").find_all("td")[5].string
    number_available = ''.join(filter(str.isdigit, availability.split()[2]))
    datas.append(number_available)
    # Ajoute la description du livre à la liste datas
    description = soup.find("p", class_=None)
    if description : 
        datas.append(description.string)
    else:    
        datas.append("")
    # Ajoute la catégorie du livre à la liste datas
    category = soup.find("ul").find_all("li")[2].find("a").string
    datas.append(category)
    # Ajoute le review rating en chiffre à la liste datas
    evaluation_avis = soup.find("p" ,class_="star-rating").get("class")[1]
    review_rating = rating_number(evaluation_avis)
    datas.append(review_rating)
    # Ajoute l'url complet de l'image 
    image_url = soup.find("div", class_="carousel-inner").find("img")["src"].strip("./")
    image_url = base_url + image_url
    datas.append(image_url)
    #  Télécharge et enregistre l'image du livre
    title_clean = re.sub(r'[\\/*?:"<>|]', "", title)
    name_file = "images/"+ category + "/" + title_clean + ".jpg"
    response = requests.get(image_url)
    with open(name_file, "wb") as picture_file:
        picture_file.write(response.content)
    return datas

# fonction permettant de récupéré un nombre a partir du dictionnaire en se servant de la variable evaluation_avis
def rating_number(evaluation_avis):
    rating_list = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    if evaluation_avis.capitalize() in rating_list:
        return rating_list[evaluation_avis]
# Ecris sur le fichiers csv les données  
def charger(file_name, datas):
    
    with open(file_name, "a", newline="", encoding="utf-8") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        writer.writerow(datas)
        
# Fonction renvoyant tout les urls des livres d'une catégorie dans une liste
def url_book_category_page(url_category):
    global base_url_category
    url_books_in_category = []
    url_pages_livres = []
    soup = sibling_url(url_category)
    nombres_page = soup.find("li", class_="current")
    if nombres_page:
        for i in range(1, (int(nombres_page.string.split()[3])+1)):
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
# Extrait les urls de chaque catégorie dans une liste
def extractions_categories(url_main):
    soup = sibling_url(url_main)
    categories = soup.find("ul", class_="nav nav-list").find_all("a")[1:]
    url_categories = {}
    urls = []
    names = []
    for category in categories :
        urls.append(base_url + "/".join(category["href"].split("/")[:-1]))
        names.append("".join(category.string.split()))
    url_categories.update({url: name for url, name in zip(urls, names)})
    print(url_categories)
        
    return url_categories

if __name__ == "__main__" : 
    # appelle la fonction pour extrait les urls des catégories
    url_categories = extractions_categories(base_url)
    # Pour chaque url des catégories appliquent le chargement de l'en tête 
    for url_category, name in url_categories.items():
        print(name)
        file_name = "datas/" + name + ".csv"
        charger(file_name, en_tete)
        # Pour chaque url des catégories, récupère les urls de chaque livre de la catégorie et si il y' a plusieurs pages les parcours   
        url_books_in_category = url_book_category_page(url_category)
        # Parcours la liste des liens de page de livre, 
        for book_url in url_books_in_category:
            print(book_url)    
            # Chaque lien de page livre est chargé dans la fonction extrayant les données du livre 
            datas = extract(book_url)
            # appelle de la fonction, pour écrire les données dans un  fichier csv
            charger(file_name,datas)
        # Une fois toute les données des livres de la même catégorie écrit dans le fichier csv le renomme par sa catégorie
    
  
            # etl(book_url) 


    
