# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exceptions import DropItem, NotConfigured
import psycopg2
from scrapy import signals
from scrapy.exporters import CsvItemExporter

# This pipeline inserts new listings into the database
class DBPipeline(object):

    def __init__(self, db, user, passwd, host, port):
        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.getdict("DB_SETTINGS")
        if not db_settings:
            raise NotConfigured
        db = db_settings['db']
        user = db_settings['user']
        passwd = db_settings['passwd']
        host = db_settings['host']
        port = db_settings['port']
        return cls(db, user, passwd, host, port)

    def open_spider(self, spider):
        self.conn = psycopg2.connect(database=self.db,
                                      host=self.host,
                                      user=self.user,
                                      password=self.passwd,
                                      port=self.port)
        self.cursor = self.conn.cursor()
        self.insert_count = 0

    def process_item(self, item, spider):
        sql = "INSERT INTO real_estate (url, city, address, area, rooms, price, property_condition, "\
              "build_year, description, floor, building_floors, property_type, advertiser_agent, "\
              "advertiser_name, time, area_lot) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"\
              " ON CONFLICT DO NOTHING;" 
        self.cursor.execute(sql,
                            (   item.get("url"),
                                item.get("city"),
                                item.get("address"),
                                item.get("area"),
                                item.get("rooms"),
                                item.get("price"),
                                item.get("property_condition"),
                                item.get("build_year"),
                                item.get("description"),
                                item.get("floor"),
                                item.get("building_floors"),
                                item.get("property_type"),
                                item.get("advertiser_agent"),
                                item.get("advertiser_name"),
                                item.get("time"),
                                item.get("area_lot"))
                            )
        sql = """
        INSERT INTO scraped_urls (url, city) VALUES (%s, %s) ON CONFLICT DO NOTHING;
        """
        self.cursor.execute(sql,
                            (item.get('url'), 
                             spider.city)
                            )
        self.insert_count += 1
        # commit in batches
        if self.insert_count == 100:
            self.insert_count = 0
            self.conn.commit()
        return item


    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

# This pipeline produces the CSV (containing URLs) that is then consumed by the spider        
class CSVPipeline(object):
    
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.file = open("url_queue_{city}.csv".format(city=spider.city), 'w+b')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

# This pipeline makes sure to only new URLs are crawled
class OnlyNewUrlsPipeline(object):

    def __init__(self, db, user, passwd, host, port):
        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.getdict("DB_SETTINGS")
        if not db_settings:
            raise NotConfigured
        db = db_settings['db']
        user = db_settings['user']
        passwd = db_settings['passwd']
        host = db_settings['host']
        port = db_settings['port']
        return cls(db, user, passwd, host, port)

    def open_spider(self, spider):
        self.conn = psycopg2.connect(database=self.db,
                                      host=self.host,
                                      user=self.user,
                                      password=self.passwd,
                                      port=self.port)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = "SELECT url FROM scraped_urls WHERE city = '{city}' AND url = '{url}'".format(
                                                                                    city=spider.city,
                                                                                    url=item.get('url'))
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        # if item is not in the database already then return it, otherwise drop
        if result is None:
            return item
        raise DropItem()


    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()
