import scrapy

class ChurchillQuotesSpider(scrapy.Spider):
    name = "citations de Churchill"
    start_urls = ["http://evene.lefigaro.fr/citations/winston-churchill",]

    def parse(self, response):
        for cit in response.xpath('//article'):

            #extraitre le texte
            text_value = cit.xpath('.//div[@class="figsco__quote__text"]/a/text()').extract_first()
            if text_value:
                #enlever les guillemets
                cleaned_text = text_value.replace("“", "").replace("”", "")

                #extraire le nom de l'auteur
                author_name = cit.css('.figsco__fake__col-9').css('a::text').extract_first()
                if author_name == "Winston Churchill":
                    yield {
                        'text': cleaned_text,
                        'author': author_name
                    }