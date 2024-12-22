class View:
    def prompt_extract_all_categories(self):
        print("l'extraction des données pour chaque catégorie du site books to scrape est en cours.")

    def prompt_extract_finish(self):
        print("Extraction réussite !!")

    def prompt_location_datas(self):
        print("Écriture des données dans un fichier csv au nom de la catégorie dans le dossier book_datas")

    def prompt_location_images(self):
        print("Enregistrement des images dans le sous-dossier d' images aux noms de leur catégorie")

    def prompt_enter_url_category(self):
        print("Vous devez fournir l'url de la catégorie.")

    def prompt_location_datas_category(self, category_name):
        print(f"Données de la catégorie {category_name} extraite dans le dossier book_datas.")

    def prompt_location_images_category(self, category_name):
        print(f"Images de la catégorie {category_name} enregistrez dans le dossier images.")

    def prompt_enter_url_book(self):
        print("Vous devez fournir l'url du livre.")

    def prompt_location_datas_book(self, title_book):
        print(f"Données du livre: {title_book} extrait dans book_datas.")


    def prompt_location_image_book(self, title_book):
        print(f"Image du livre: {title_book} enregistré dans le dossier images.")

    def prompt_invalid_action(self, action):
        print(f"Action inconnue : {action}. utilisez category ou book")
