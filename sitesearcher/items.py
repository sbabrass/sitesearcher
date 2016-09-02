# -*- coding: utf-8 -*-

import scrapy


class SearchItem(scrapy.Item):
    """ Model for Scrapy search items.

    Contains simply the url and the cleaned-up full-text content of the
    crawled site.
    """

    url = scrapy.Field()
    content = scrapy.Field()
    # modified = scrapy.Field()
