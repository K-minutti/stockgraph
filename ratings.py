import scrapy


class RatingsSpider(scrapy.Spider):
    name = 'ratingsspider'
    start_urls = ['https://finviz.com/quote.ashx?t=SYPR']

    def parse(self, response):
        for table in response.css('td.fullview-ratings-inner'):
            yield {'rating': table.xpath('/td[@align="left"]/text()').get()}
