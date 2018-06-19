from scrapy.spiders import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.item import Item
from urllib.parse import urljoin
import re
import scrapy

class newspider(BaseSpider):
    name = 'newspider'
    allowed_domains = ['www.adaderana.lk']
    start_urls = ['http://www.adaderana.lk/']

    seen = set()

    def parse(self, response):
        if response.url in self.seen:
            self.log('already seen  %s' % response.url)
        else:
            self.log('parsing  %s' % response.url)
            self.seen.add(response.url)

        hxs = HtmlXPathSelector(response)
        self.log("Response URL " + response.url)
        if re.match(r'https://www.icc-cricket.com/news/\d{6}/\w', response.url):
            yield {
                    'title': hxs.select('/html/body/div[5]/div/div[1]/article/h1').extract_first(),
                    'content': hxs.select('/html/body/div[5]/div/div[1]/article/div[10]').extract_first(),
                    'author': hxs.select('/html/body/div[5]/div/div[1]/article/div[8]/p/a').extract_first(),
                    'url': response.url,
                }

        #     

        for url in hxs.xpath('//a/@href').extract():
            url = urljoin(response.url, url)
            if not url in self.seen and not re.search(r'.(pdf|zip|jar)$', url):
                #self.log("yielding request " + url)
                yield scrapy.Request(url, callback=self.parse)
