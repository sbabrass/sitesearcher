import re
from whoosh.highlight import Formatter
from whoosh.highlight import get_text
from scrapy.settings import Settings


def get_user_agent():
    """ Return the User Agent string.

    Separated to support extensions in later versions.
    """

    return "SiteSearcher"


def decode(string, encoding):
    """ Handle Python 2 + 3 compatibility issue """
    try:
        # For Python 2
        return string.decode(encoding)
    except AttributeError:
        # For Python 3
        return string


def clean_response_body(body):
    """ Remove HTML tags and unnecessary whitespaces. """

    body = decode(body, 'utf-8')
    body = re.sub("<.*?>", " ", body)
    body = re.sub("\s\s+", " ", body)
    return body


class ConsoleFormatter(Formatter):
    """Returns a string in which the matched terms wrapped in XML-like tags.
    """

    def __init__(self, between="..."):
        """
        :param between: the text to add between fragments.
        """

        self.between = between

    def format_token(self, text, token, replace=False):
        ttxt = get_text(text, token, replace)
        return u"<searchphrase>{}</searchphrase>".format(ttxt)


def get_project_settings():
    """ Get Scrapy Settings for SiteSearcher """

    settings = Settings()
    settings.setmodule('sitesearcher.settings', priority='project')

    return settings
