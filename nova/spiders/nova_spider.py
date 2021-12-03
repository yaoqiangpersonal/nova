import scrapy
import re

class NovaSpiderSpider(scrapy.Spider):
    name = 'nova_spider'
    allowed_domains = ['novamnm.com']
    start_urls = ['http://novamnm.com/']
    proxy = "192.168.1.199:7890"

    def start_requests(self):
        for page in range(1,14):
            yield scrapy.Request("https://novamnm.com/category/winter-festival/122/?page=" + str(page), 
                               method="GET",
                                meta={"proxy": self.proxy},
                                callback=self.parse)

    def parse(self, response):
        if(response.url.find('page') > 0):
            results = response.css('#prdList ul .box .thumbbox::attr(href)').getall()
            yield from response.follow_all(results, meta={"proxy": self.proxy})
        else:
            title = response.css('.headingArea h2::text').get()
            price = response.css('meta[property$=amount]::attr(content)').getall()[1]
            yield {
                'path':response.url,
                'title':title,
                'price':price
            }
