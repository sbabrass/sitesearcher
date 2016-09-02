import re
import scrapy
from datetime import datetime
from email.utils import parsedate
from sitesearcher.items import SearchItem
from sitesearcher.utils import clean_response_body
from sitesearcher.utils import decode

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

    def parse(self, response):
        item = SearchItem()
        item['url'] = decode(response.url, 'utf-8')
        item['content'] = clean_response_body(response.body)
        # if 'Last-Modified' in response.headers:
        #     import pdb; pdb.set_trace();
        #     item['modified'] = datetime(
        #         *parsedate(response.headers['Last-Modified'])[:6])
        yield item
        for linkobj in response.css('a::attr("href")'):
            url = response.urljoin(linkobj.extract())
            yield scrapy.Request(url, callback=self.parse)

