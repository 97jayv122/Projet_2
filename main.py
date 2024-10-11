import csv
import requests
from bs4 import BeautifulSoup

def extraire(url):
    response = requests.get(url)
    page = response.content
    soup = BeautifulSoup(page, "html.parser")
    titre_livre = soup.h1.string
    produit_description = soup.p.string
    print(produit_description)
    elements_tableau = soup.find_all("tr")
    return titre_livre, produit_description, elements_tableau
    
def transformer(element):
    titres_tableau = element.find("th")
    descriptions_tableau = element.find("td")
    return (titres_tableau.string, descriptions_tableau.string)

def charger(page_product_url, titre_livre, produit_descrption, en_tete, donnees, ):
    with open("data.csv", "w", newline="") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        writer.writerow(page_product_url)
        writer.writerow(titre_livre)
        writer.writerow(produit_descrption)
        writer.writerow(en_tete)
        for donnee in donnees:
            writer.writerow(donnee)
def etl(url):
    page_product_url =["page_product_url", url] 
    
    titre_livre, produit_description, elements_tableau = extraire(url)
    titre_livre = ["livre", titre_livre]
    produit_description = ["produit_description", produit_description]
    produit_informations = [transformer(element) for element in elements_tableau]
    en_tete = ["titres", "descriptions"]
    charger(page_product_url, titre_livre, produit_description, en_tete, produit_informations)

if __name__ == "__main__" : 
    etl("https://books.toscrape.com/catalogue/scott-pilgrims-precious-little-life-scott-pilgrim-1_987/index.html")       
