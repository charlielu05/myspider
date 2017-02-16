import scrapy
import pandas
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
import datetime

class REItem(scrapy.Item):
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
    bond = scrapy.Field()

class RealSpider(scrapy.Spider):
    name = 'RE-Rent'
    allowed_domains = ['realestate.com.au']
    start_urls = ["http://www.realestate.com.au/rent/in-tarragindi%2c+qld+4121%3b+/list-1?includeSurrounding=false&source=location-search", "http://www.realestate.com.au/rent/in-sunnybank%2c+qld+4109/list-1?includeSurrounding=false&persistIncludeSurrounding=true&source=location-search"
                  ,"http://www.realestate.com.au/rent/in-sunnybank+hills%2c+qld+4109/list-1?includeSurrounding=false&source=location-search"
                  ,"http://www.realestate.com.au/rent/in-eight+mile+plains/list-1?includeSurrounding=false&source=location-search"
                  ,"http://www.realestate.com.au/rent/in-mount+gravatt%2c+qld+4122%3b+/list-1?includeSurrounding=false&source=location-search"
                  ,"http://www.realestate.com.au/rent/in-greenslopes%2c+qld+4120%3b+/list-1?includeSurrounding=false&source=location-search"
                  ,"http://www.realestate.com.au/rent/in-holland+park+west%2c+qld+4121%3b+/list-1?includeSurrounding=false&source=location-search"
                  ,"http://www.realestate.com.au/rent/in-coorparoo%2c+qld+4151%3b+/list-1?includeSurrounding=false&source=location-search"
                  ]
    # start_urls = [
    #     #"http://www.realestate.com.au/buy/in-tarragindi%2c+qld+4121%3b+/list-1?includeSurrounding=false&source=location-search",
    #     "http://www.realestate.com.au/buy/in-sunnybank%2c+qld+4109/list-1?includeSurrounding=false&persistIncludeSurrounding=true&source=location-search"
    #     ]
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
            bond = response.xpath("//li[contains(., 'Bond:')]//span/text()").extract()[0]
        except IndexError:
            bond = ''
        try:
            land = response.xpath("//li[contains(., 'Land Size:')]//span/text()").re('(\d+)')[0]
        except IndexError:
            try:
                land = response.css('ul.additionalInfo ::text').extract()[2]
            except IndexError:
                land = ''
        try:
            garage = response.css('dl.rui-property-features.rui-clearfix dd::text')[2].extract()
        except IndexError:
            try:
                garage = response.xpath('//ul[@class="features"]/li[@class="cars rui-icon rui-icon-car"]/text()').extract()[0]
            except IndexError:
                garage = ''
        try:
            bedroom = response.css('dl.rui-property-features.rui-clearfix dd::text')[0].extract()
        except IndexError:
            try:
                bedroom = response.xpath('//ul[@class="features"]/li[@class="beds rui-icon rui-icon-bed"]/text()').extract()[0]
            except IndexError:
                bedroom = ''
        try:
            bathroom = response.css('dl.rui-property-features.rui-clearfix dd::text')[1].extract()
        except IndexError:
            try:
                bathroom = response.xpath('//ul[@class="features"]/li[@class="baths rui-icon rui-icon-bath"]/text()').extract()[0]
            except IndexError:
                bathroom = ''
        try:
            pid = response.css('span.property_id ::text').re('(\d+)')[0]
        except IndexError:
            pid = re.search('\d+', response.url)
            pid = pid.group(0)
        try:
            price = response.css('li.price p::text').extract()[0]
        except IndexError:
            try:
                price = response.xpath('//p[@class="heading price"]/span/text()').extract()[0].strip()
            except IndexError:
                price = ''
        try:
            street = response.xpath('//h1[@itemprop="address"]/span[@itemprop="streetAddress"]/text()').extract()[0]
        except IndexError:
            try:
                street = response.xpath('//div[@class="secondaryBlock"]/p[@class="address"]/span/text()').extract()[0]
            except IndexError:
                street = ''
        try:
            state = response.xpath('//h1[@itemprop="address"]/span[@itemprop="addressRegion"]/text()').extract()[0]
        except IndexError:
            state = ''
        try:
            suburb = response.xpath('//h1[@itemprop="address"]/span[@itemprop="addressLocality"]/text()').extract()[0]
        except IndexError:
            suburb = ''
        try:
            postcode = response.xpath('//h1[@itemprop="address"]/span[@itemprop="postalCode"]/text()').extract()[0]
        except IndexError:
            postcode = ''
        try:
            typeof = response.xpath('//li[@class="property_info"]/span[@class="propertyType"]/text()').extract()[0]
        except IndexError:
            try:
                typeof = response.xpath('//div[@class="secondaryBlock"]/ul[@class="clear"]/li/text()').extract()[0]
            except IndexError:
                typeof = ''
        item['postcode'] = postcode
        item['suburb'] = suburb
        item['state'] = state
        item['land'] = land
        item['street'] = street
        item['price'] = price
        item['pid'] = pid
        item['bedroom'] = bedroom
        item['garage'] = garage
        item['bathroom'] = bathroom
        item['typeof'] = typeof
        item['url'] = response.url
        item['day'] = datetime.datetime.now()
        item['bond'] =bond
        #item['body'] = response.css('p.body ::text').extract()
        return item

