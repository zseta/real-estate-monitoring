import os
from real_estate.items import RealEstateItem
from scrapy.http.request import Request
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from scrapy.spiders import Spider
from w3lib.html import remove_tags
from datetime import datetime
import csv

class RealEstate(Spider):
    name = 'real_estate'
    start_urls = [] # this value will be overwritten in the start_requests function below
    city = None
    custom_settings = {
        'ITEM_PIPELINES': {
            'real_estate.pipelines.DBPipeline': 301
        }
    }
    
    # consumes the CSV file produced by real_estate_discover spider
    # and uses those URL values for the requests
    def _get_urls_from_queue(self,):
        csv_path = "url_queue_{city}.csv".format(city=self.city)
        with open(csv_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader) # skip header
            urls = list(csv_reader)
            return [url[1] for url in urls]
    
    def start_requests(self):
        self.city = getattr(self, 'city', None)
        if self.city is None:
            raise ValueError("You must provide 'city' parameter! eg. -a city='budapest'")
        self.start_urls = self._get_urls_from_queue()
        for url in self.start_urls:
            yield Request(url)

    def parse(self, response):
        loader = ItemLoader(item=RealEstateItem(), response=response)
        loader.default_input_processor = MapCompose(remove_tags)
        loader.default_output_processor = TakeFirst()

        address_css = "h1.address"
        loader.add_css('address', address_css)
        loader.add_css('city', address_css)
        
        loader.add_css('property_type', "div.digest")
        
        parameters_css = "div.parameters > div.parameter > div.parameterValues > span:first-of-type"
        loader.add_css('area', parameters_css)
        loader.add_css('area_lot', parameters_css)
        loader.add_css('price', parameters_css)
        loader.add_css('rooms', parameters_css)
        
        loader.add_xpath('property_condition', self.get_xpath("Ingatlan állapota"))
        loader.add_xpath('build_year', self.get_xpath("Építés éve"))
        loader.add_xpath('floor', self.get_xpath("Emelet"))
        loader.add_xpath('building_floors', self.get_xpath("Épület szintjei"))
        
        loader.add_css('description', "div.longDescription")
        loader.add_css('advertiser_agent', "div.listingOwnerIdentity > div > div.officeName")
        loader.add_css('advertiser_name', "div.listingOwnerIdentity > div > div.name")
        
        loader.add_value('url', response.url)
        loader.add_value('time', datetime.now())
        yield loader.load_item()
        
    def get_xpath(self, text):
        return "//dt[@class='parameterName'][contains(text(), '{text}')]"\
               "//following-sibling::dd[1]".format(text=text)
               
    # CSV can be deleted once this job is over
    def closed(self, reason):
        queue_file = "url_queue_{city}.csv".format(city=self.city)
        if os.path.exists(queue_file):
            os.remove(queue_file)