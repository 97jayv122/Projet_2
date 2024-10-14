import csv
import requests
from bs4 import BeautifulSoup

def extraire(url):
    response = requests.get(url)
    page = response.content
    soup = BeautifulSoup(page, "html.parser")
    titre_livre = soup.h1.string
    produit_description = soup.find("p", class_=None)
    produit_description = produit_description.string
    categorie = soup.find("ul").find_all("li")[2].find("a").string
    evaluation_avis = soup.find("p" ,class_="star-rating")
    evaluation_avis = evaluation_avis.get("class")[1]
    elements_tableau = soup.find_all("tr")
    return evaluation_avis, categorie, titre_livre, produit_description, elements_tableau
    
def transformer(element):
    titres_tableau = element.find("th")
    descriptions_tableau = element.find("td")
    return (titres_tableau.string, descriptions_tableau.string)

def charger(page_product_url, titre_livre, produit_descrption, categorie, evaluation_avis, en_tete, donnees, ):
    with open("data.csv", "w", newline="") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        writer.writerow(page_product_url)
        writer.writerow(titre_livre)
        writer.writerow(produit_descrption)
        writer.writerow(categorie)
        writer.writerow(evaluation_avis)
        writer.writerow(en_tete)
        for donnee in donnees:
            writer.writerow(donnee)
def etl(url):
    page_product_url =["Page_product_url", url] 
    evaluation_avis, categorie, titre_livre, produit_description, elements_tableau = extraire(url)
    titre_livre = ["Livre", titre_livre]
    produit_description = ["Produit_description", produit_description]
    produit_informations = [transformer(element) for element in elements_tableau]
    categorie = ["Catégorie", categorie]
    evaluation_avis = ["Evaluation_avis", evaluation_avis]
    en_tete = ["Titres", "Descriptions"]
    charger(page_product_url, titre_livre, produit_description, categorie, evaluation_avis, en_tete, produit_informations)

if __name__ == "__main__" : 
    etl("https://books.toscrape.com/catalogue/scott-pilgrims-precious-little-life-scott-pilgrim-1_987/index.html")       
