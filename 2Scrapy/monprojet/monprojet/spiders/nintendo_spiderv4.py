import scrapy
from scrapy import Request
from ..items import ArticleItem

class NintendoSpider(scrapy.Spider):
    name = "nintendo_spiderv4"
    allowed_domains = ["nintendo.com"]
    start_urls = ['https://www.nintendo.com/fr-fr/Jeux/']

    def parse(self, response, **kwargs):
        """
        Parse la page contenant la liste des jeux et envoie une requête pour chaque jeu.
        """
        # Trouver tous les liens vers les pages individuelles des jeux
        game_links = response.css('.game-card a::attr(href)').extract()

        # Pour chaque lien de jeu, on fait une requête pour récupérer les informations
        for link in game_links:
            yield Request(response.urljoin(link), callback=self.parse_game)

    def parse_game(self, response):
        """
        Parse la page de chaque jeu pour extraire les informations spécifiques.
        """
        title = self.clean_spaces(response.css("h1.title span::text").extract_first())
        description = self.clean_spaces(response.css(".description span::text").extract_first())
        image_url = response.css(".hero-image img::attr(src)").extract_first()

        # Vérifier si l'image est un lien relatif et la convertir en absolu
        if image_url:
            image_url = response.urljoin(image_url)

        # Créer un objet ArticleItem et y ajouter les informations extraites
        yield ArticleItem(
            title=title,
            image=image_url,
            description=description
        )

    def clean_spaces(self, string):
        """
        Nettoie les espaces superflus dans une chaîne de caractères.
        """
        if string:
            return " ".join(string.split())
        return string



