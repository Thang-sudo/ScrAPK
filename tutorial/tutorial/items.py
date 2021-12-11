# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class AppItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    distributor = Field()
    link = Field()
    title = Field()
    path_title = Field()
    developer = Field()
    package_name = Field()
    
    
