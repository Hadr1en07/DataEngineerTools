import scrapy


class NintendoSpiderv1Spider(scrapy.Spider):
    name = "nintendo_spiderv1"
    allowed_domains = ["www.nintendo.fr"]
    start_urls = ["https://nintendo.fr/fr-fr"]

    def parse(self, response):
        pass
