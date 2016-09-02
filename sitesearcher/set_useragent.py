#-*-coding:utf-8-*-

from scrapy import log
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from sitesearcher.utils import get_user_agent


class SetUserAgentMiddleware(UserAgentMiddleware):
    """ Middleware to create a new random useragent for each request. """

    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        ua = get_user_agent()
        if ua:
            request.headers.setdefault('User-Agent', ua)

        spider.log(
            u'User-Agent: {} {}'.format(request.headers.get('User-Agent'), request),
            level=log.DEBUG
        )
