import scrapy 
from scrapy.crawler import CrawlerProcess 

def get_ratings(symbol):
    class Ratings_Spider(scrapy.Spider):
        name = "ratings_spider"

        def start_requests(self):
            url = f'https://finviz.com/quote.ashx?t={symbol}&ty=c&ta=1&p=d'
            yield scrapy.Request(url = url, callback = self.parse)

        def parse(self, response):
            print("\n")
            print("HTTP STATUS "+str(response.status))
            inner_tables = response.css("table.fullview-ratings-outer tr table")
            for table in inner_tables:
                rows = table.xpath('tr[contains(@class, "body-table-rating")]//td//text()').extract()
                ratings.append(rows)
            print("\n")

    ratings = []

    process = CrawlerProcess()
    process.crawl(Ratings_Spider)
    process.start()
    return ratings

