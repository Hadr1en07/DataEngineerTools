import scrapy
from scrapy import Request


class NintendoSpider(scrapy.Spider):
    name = "nintendo_spiderv2"
    allowed_domains = ["www.nintendo.com"]
    start_urls = ["https://www.nintendo.com/fr-fr/Jeux/Jeux-347085.html"]

    def parse(self, response):
        #extraction des jeux listés sur la page
        games = response.css('.page-list-group-item')

        for game in games:
            title = game.css('.page-title::text').get().strip()  #titre du jeu
            description = game.css('.page-description span::text').get(default="").strip()  #description du jeu
            relative_url = game.css('.page-img a::attr(href)').get() #url relatif
            absolute_url = response.urljoin(relative_url)

            yield {
                "title": title,
                "description": description,
                "url": absolute_url,
            }