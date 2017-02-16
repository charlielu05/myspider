import scrapy

class REItem(scrapy.Item):
    price = scrapy.Field()
    address = scrapy.Field()
    bedroom = scrapy.Field()
    bathroom = scrapy.Field()
    garage = scrapy.Field()

class RealSpider(scrapy.Spider):
    name = 'RE3'
    allowed_domains = ['realestate.com.au']
    start_urls = ["http://www.realestate.com.au/buy/property-house-in-tarragindi%2c+qld+4121/list-1?includeSurrounding=false&persistIncludeSurrounding=true&source=location-search"
                  ]

    def parse(self, response):
        for sel in response.css('div.listingInfo.rui-clearfix'):
            item = REItem()
            item['price'] = sel.css('.propertyStats p::text').extract()
            item['address'] = sel.css('div.vcard h2 a::text').extract()
            item['bedroom'] = sel.css('dl.rui-property-features.rui-clearfix dd::text')[0].extract()
            item['bathroom'] = sel.css('dl.rui-property-features.rui-clearfix dd::text')[1].extract()
            item['garage'] = sel.css('dl.rui-property-features.rui-clearfix dd::text')[2].extract()
            yield item

        next_page = response.css('li.nextLink a ::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )