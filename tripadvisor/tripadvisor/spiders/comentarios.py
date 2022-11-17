import scrapy
from ..items import TripadvisorItem

class ComentariosSpider(scrapy.Spider):
    name = 'comentarios'
    allowed_domains = ['tripadvisor.com.br']
    start_urls = ['https://www.tripadvisor.com.br/Attraction_Review-g4084093-d2405960-Reviews-Serra_do_Rio_do_Rastro-Lauro_Muller_State_of_Santa_Catarina.html']

    def parse(self, response):
        item = TripadvisorItem()
        quadros_de_comentarios = response.xpath("//div[@class = '_c']")
        for quadro in quadros_de_comentarios:
            item["autor_comentario"] = quadro.xpath(".//div[@class ='zpDvc']/span/a/text()").get()
            item["autor_endereco"] = quadro.xpath(".//div[@class='JINyA']/div/span/text()").get()
            item["comentario_titulo"] = quadro.xpath(".//div[@class='biGQs _P fiohW qWPrE ncFvv fOtGX']/a/span/text()").get()
            item["comentario_corpo"] = quadro.xpath(".//div[@class='fIrGe _T bgMZj']/div/span/text()").get()
            item["comentario_data"] = quadro.xpath(".//div[@class='RpeCd']/text()").get()
            yield item

        next_page = response.xpath("//div[@class='xkSty']/div/a/@href").get()
        if next_page:
            yield response.follow(url = next_page, callback = self.parse)
