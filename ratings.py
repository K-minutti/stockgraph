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
            row = table.css("tr")
            elems = row.css("td")
            ratings.append(elems)
        print("\n")
        #pull text from the Selector objects in elems
        # for table in inner_tables:
        #     ratings.append({"date":, "status":, "institution":, "rating":, "target":})

        # <tr class="body-table-rating-neutral">
        #   <td width="120" align="left">Dec-09-20</td>
        #   <td width="200" align="left"><b>Reiterated</b></td>
        #   <td width="250" align="left">Wedbush</td>
        #   <td width="250" align="left">Outperform</td>
        #   <td width="150" align="left">$150 &rarr; $160</td>
        # </tr>




ratings = []

process = CrawlerProcess()
process.crawl(Ratings_Spider)
process.start()

print(ratings)