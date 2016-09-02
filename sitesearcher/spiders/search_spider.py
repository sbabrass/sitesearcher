import re
import scrapy
from datetime import datetime
from email.utils import parsedate
from sitesearcher.items import SearchItem
from sitesearcher.utils import clean_response_body
from sitesearcher.utils import decode
from scrapy.http import Request


class SearchSpider(scrapy.Spider):
    """ The SiteSearcher spider.

    Follows every link on every site within the search domain and returns
    site items to the pipeline.
    """
    name = "search"
    custom_settings = {
        'ITEM_PIPELINES': {
           'sitesearcher.pipelines.SearchPipeline': 300,
        }
    }
    # state = {
    #     'update_list': [],
    # }

    def parse(self, response):
        item = SearchItem()
        item['url'] = decode(response.url, 'utf-8')
        item['content'] = clean_response_body(response.body)
        if 'update_list' in self.state:
            self.state['update_list'].append(item.get('url'))
        else:
            self.state['update_list'] = [item.get('url')]
        # if 'Last-Modified' in response.headers:
        #     item['modified'] = datetime(
        #         *parsedate(response.headers['Last-Modified'])[:6])
        yield item
        for linkobj in response.css('a::attr("href")'):
            url = response.urljoin(linkobj.extract())
            yield scrapy.Request(url, callback=self.parse)

    def start_requests(self):
        # Override to enable duplicate filtering of start urls
        for url in self.start_urls:
            yield Request(url)
