import scrapy

class REItem(scrapy.Item):
    price = scrapy.Field()
    address = scrapy.Field()

class RealSpider(scrapy.Spider):
    name = 'RE2'
    allowed_domains = ['realestate.com.au']
    start_urls = ["http://www.realestate.com.au/buy/property-house-in-tarragindi%2c+qld+4121/list-1?includeSurrounding=false&persistIncludeSurrounding=true&source=location-search"
                  ]

    def parse(self, response):

        prices = response.css('.propertyStats p::text').extract()
        addresses = response.css('div.vcard h2 a::text').extract()
        for price in prices:
            item = REItem()
            item['price'] = price
            yield item
        for address in addresses:
            item = REItem()
            item['address'] = address
            yield item

