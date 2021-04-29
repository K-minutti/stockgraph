import scrapy 
from scrapy.crawler import CrawlerProcess 

class Ratings_Spider(scrapy.Spider):
    name = "ratings_spider"

    def start_requests(self):
        url = 'https://finviz.com/quote.ashx?t=AAPl&ty=c&ta=1&p=d'
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


#we want a to call this fucntion with the symbol
#and if there is not ratings table we exit and return the message not ratings available
#[[1,2,3], [1,2,3]]
#for ratings in ratings pull the data as rating[1], rating[2]
#display in the front-end

