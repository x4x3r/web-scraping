from time import strptime
from datetime import datetime
import scrapy
from scrapy import spiders
from scrapy.selector.unified import _response_from_text
from scrapy.spiders import Spider
from ealatihr.items import EalatihrItem
from scrapy.extensions import corestats


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['ealati.hr']
    """ start_urls = ['https://www.ealati.hr/kategorija-proizvoda/vrtni-asortiman/',
                  'https://www.ealati.hr/kategorija-proizvoda/akumulatorski-alati/',
                  'https://www.ealati.hr/kategorija-proizvoda/elektricni-alati/',
                  'https://www.ealati.hr/kategorija-proizvoda/kompresori-i-pneumatski-alati/',
                  'https://www.ealati.hr/kategorija-proizvoda/zavarivanje-i-oprema/',
                  'https://www.ealati.hr/kategorija-proizvoda/strojevi-i-uredaji/'] """
    
    start_urls = ['https://www.ealati.hr/kategorija-proizvoda/vrtni-asortiman/kosilice/elektricne-kosilice/'] 
    
    def parse(self, response):
        product_links = response.css('.product-loop-header a.woocommerce-LoopProduct-link')
        yield from response.follow_all(product_links, callback=self.parse_product)

        next_pages = response.css('a[class=page-numbers]')
        yield from response.follow_all(next_pages, callback=self.parse)
    
    @classmethod
    def spider_closed(cls, spider, reason):
        finish_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return finish_time

    def parse_product(self, response):
        productItem = EalatihrItem()
        productItem['listingUrl'] = response.css('.woocommerce-breadcrumb a:nth-of-type(2)::attr(href)').get()
        productItem['productUrl'] = response.url
        productItem['sku'] = response.css('span.sku::text').get()
        productItem['category'] = response.css('.posted_in a::text').getall()
        productItem['brand'] = response.css('.tagged_as a::text').get()
        productItem['price'] = response.css('p bdi::text').get()
        productItem['oldPrice'] = response.css('p del bdi::text').get()
        productItem['images'] = response.css('img::attr(data-large_image)').getall()
        productItem['specsTable'] = response.css('.ealati_specifikacija span::text').getall()
        productItem['crawledAt'] = self.spider_closed(self, reason=response.request.meta['depth'])
        return productItem