# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class item(scrapy.Item):
    price = scrapy.Field()
    street = scrapy.Field()
    suburb = scrapy.Field()
    state = scrapy.Field()
    postcode = scrapy.Field()
    bedroom = scrapy.Field()
    bathroom = scrapy.Field()
    garage = scrapy.Field()
    land = scrapy.Field()
    pid = scrapy.Field()
    typeof = scrapy.Field()
    body = scrapy.Field()
    url = scrapy.Field()
    day = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
