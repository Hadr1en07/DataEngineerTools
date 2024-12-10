import scrapy
from scrapy import Request
import json

class NintendoSpider(scrapy.Spider):
    name = "nintendo_spiderv3"
    allowed_domains = ["nintendo.com"]
    start_urls = ['https://www.nintendo.com/fr-fr/Jeux/Jeux-347085.html']

    def parse(self, response):
        """
        Parse la page principale pour collecter les liens vers les jeux.
        """
        # Extraire tous les liens des jeux sur la page principale
        game_links = response.css(
            "li.page-list-group-item a::attr(href)"
        ).extract()

        # Suivre chaque lien pour extraire des détails sur le jeu
        for link in game_links:
            full_url = response.urljoin(link)
            yield Request(full_url, callback=self.parse_game)

    def parse_game(self, response):
        """
        Parse une page de détail d'un jeu pour en extraire des informations.
        """
        # Extraire les informations principales visibles
        title = response.css(".page-title::text").get(default="").strip()
        image = response.css(".page-container img::attr(data-sm)").get()
        description = response.css(".page-description span::text").get(default="").strip()

        # Extraire les informations spécifiques au jeu depuis le `dataLayer`
        data_layer = self.extract_data_layer(response)
        if data_layer:
            price = data_layer.get("offdeviceProductPrice", None)
            nsuid = data_layer.get("offdeviceNsuID", None)
            genre = data_layer.get("gameGenre", "").replace("|", ", ").strip(", ")
            age_rating = data_layer.get("gameAgeRatingValue", None)
            franchise = data_layer.get("gameFranchise", "").replace("|", ", ").strip(", ")
        else:
            price = nsuid = genre = age_rating = franchise = None

        # Retourner les données sous forme de dictionnaire
        yield {
            "title": title,
            "image": image,
            "description": description,
            "price": price,
            "nsuid": nsuid,
            "genre": genre,
            "age_rating": age_rating,
            "franchise": franchise,
            "url": response.url,
        }

    def extract_data_layer(self, response):
        """
        Parse le `dataLayer` JavaScript pour extraire les données pertinentes.
        """
        script_text = response.xpath(
            "//script[contains(text(), 'window.dataLayer.push')]/text()"
        ).get()

        if script_text:
            try:
                # Isoler le JSON dans la fonction push()
                json_start = script_text.find("window.dataLayer.push({") + 22
                json_end = script_text.find("});", json_start)
                json_text = script_text[json_start:json_end]

                # Charger le JSON en tant que dictionnaire Python
                return json.loads(json_text)
            except (ValueError, json.JSONDecodeError):
                self.logger.warning("Impossible de décoder le JSON du dataLayer.")
                return None
        return None