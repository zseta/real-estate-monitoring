from scrapy.spiders import Spider
from real_estate.items import RealEstateUrlItem
from bs4 import BeautifulSoup
import requests
from scrapy import Request


class RealEstateDiscover(Spider):
    name = 'real_estate_discover'
    start_urls = ["website.com", # include websites you want to scrape
                  "website.com"]
    city = None
    custom_settings = {
        'ITEM_PIPELINES': {
            'real_estate.pipelines.OnlyNewUrlsPipeline': 301,
            'real_estate.pipelines.CSVPipeline': 302,
        }
    }

    def start_requests(self):
        self.city = getattr(self,'city','')
        if self.city == '':
            raise ValueError("You must provide 'city' parameter! eg. -a city='budapest'")
        for url in self.start_urls:
            max_page = 100 # extract listings from the first 100 pages (modify to fit your needs)
            
            # it's assumed that you'll be able to paginate using a pattern like 'site.com/page1 .. page2 .. page2 etc'
            # if that's not the case you need to change this pagination logic
            for page_number in range(1, max_page+1):
                if page_number == 1:
                    yield Request(url + self.city)
                else:
                    yield Request(url + "{city}?page={page}".format(city=self.city, page=page_number))

    def parse(self, response):
        for listing in response.css(".listing__link"):  # define a "box" which contains the fields for ONE SINGLE item
            item = RealEstateUrlItem()
            item['url'] = response.urljoin(listing.css("a::attr(href)").get())
            item['city'] = self.city
            yield item
