import scrapy

class REItem(scrapy.Item):
    price = scrapy.Field()
    street = scrapy.Field()
    suburb = scrapy.Field()
    state =scrapy.Field()
    postcode = scrapy.Field()
    bedroom = scrapy.Field()
    bathroom = scrapy.Field()
    garage = scrapy.Field()
    land = scrapy.Field()
    id = scrapy.Field()
    type = scrapy.Field()
    body = scrapy.Field()

class RealSpider(scrapy.Spider):
    name = 'RE-Spider'
    allowed_domains = ['realestate.com.au']
    start_urls = ["http://www.realestate.com.au/buy/in-tarragindi%2c+qld+4121%3b+/list-1?includeSurrounding=false&source=location-search", "http://www.realestate.com.au/buy/in-sunnybank%2c+qld+4109/list-1?includeSurrounding=false&persistIncludeSurrounding=true&source=location-search"
                  ]
    BASE_URL = 'http://www.realestate.com.au'

    def parse(self, response):
        links = response.css('h2.rui-truncate a ::attr(href)').extract()
        for link in links:
            absolute_url = self.BASE_URL + link
            yield scrapy.Request(absolute_url, callback=self.parse_attr)

        next_page = response.css('li.nextLink a ::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_attr(self, response):
        item = REItem()
        try:
            land = response.xpath('//*[(@id = "features")]//li[(((count(preceding-sibling::*) + 1) = 5) and parent::*)]//span/text()').extract()
        except IndexError:
            land = 'null'
        try:
            garage = response.css('dl.rui-property-features.rui-clearfix dd::text')[2].extract()
        except IndexError:
            garage = 'null'
        try:
            bedroom = response.css('dl.rui-property-features.rui-clearfix dd::text')[0].extract()
        except IndexError:
            bedroom = 'null'
        try:
            bathroom = response.css('dl.rui-property-features.rui-clearfix dd::text')[1].extract()
        except IndexError:
            bathroom = 'null'
        item['bedroom'] = bedroom
        item['garage'] = garage
        item['land'] = land
        item['bathroom'] = bathroom
        item['price'] = response.css('li.price p::text').extract()
        item['suburb'] = response.xpath('//*[(@id = "listing_header")]//span[(((count(preceding-sibling::*) + 1) = 2) and parent::*)]/text()').extract()
        item['state'] = response.xpath('//*[(@id = "listing_header")]//span[(((count(preceding-sibling::*) + 1) = 3) and parent::*)]/text()').extract()
        item['postcode'] = response.xpath('//*[(@id = "listing_header")]//span[(((count(preceding-sibling::*) + 1) = 4) and parent::*)]/text()').extract()
        item['street'] = response.xpath('//h1//span[(((count(preceding-sibling::*) + 1) = 1) and parent::*)]/text()').extract()
        item['id'] = response.css('span.property_id ::text').extract_first()
        item['type'] = response.css('span.propertyType ::text').extract()
        item['body'] = response.css('p.body ::text').extract()
        return item

