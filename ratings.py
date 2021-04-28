import scrapy 

class RatingsSpider(scrapy.Spider):
    name='rating_spider'

    start_urls = ['https://finviz.com/quote.ashx?t=AAPl&ty=c&ta=1&p=d']

    def parse(self, response):
        print("\n")
        print("HTTP STATUS "+str(response.status))
        table = response.css("table.fullview-ratings-outer") #getting the main ratings table
        statuses = table.css("b")
        print(statuses)
        print("\n")
        