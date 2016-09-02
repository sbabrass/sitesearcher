
import click
import re
import os
import shutil
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
    from urllib.request import Request
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
    from urllib2 import Request
from scrapy.crawler import CrawlerProcess
from whoosh import index
from whoosh.qparser import QueryParser
from whoosh.index import EmptyIndexError
from sitesearcher.utils import get_user_agent
from sitesearcher.utils import clean_response_body
from sitesearcher.utils import ConsoleFormatter
from sitesearcher.utils import get_project_settings


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def sitesearcher():
    """SiteSearcher

    A command line tool to search your favorite websites locally from your
    machine.

    Start by building an index for the website you want to search:

    sitesearcher indexer <domain>

    Depending on the size of your chosen site, this may take a while.
    Following this you can go on searching with:

    sitesearcher search <domain>
    """

    pass


@sitesearcher.command()
@click.argument('domain', metavar="<domain>")
@click.option('--continue', '-c', 'continued', is_flag=True,
              help='Continue previously aborted indexing')
def indexer(domain, continued):
    """ Build or update the search index for the website.

    To pause indexing press CTRL+C once and wait for graceful exit.
    Use the --continue flag to continue a paused indexing process.
    """
    path = os.path.expanduser('~/.sitesearcher/tmp-{}'.format(domain))

    if not continued:
        try:
            shutil.rmtree(path)
        except OSError:
            pass

    settings = get_project_settings()
    settings['JOBDIR'] = path
    process = CrawlerProcess(settings)
    process.crawl(
        'search',
        allowed_domains=[domain],
        start_urls=["http://{}".format(domain)]
    )
    click.echo('Building the index...')
    process.start()
    click.echo('Index is now up to date!')


@sitesearcher.command()
@click.argument('domain', metavar="<domain>")
def search(domain):
    """ Search your indexed website. """

    # Look for index for requested domain
    try:
        ix = index.open_dir(
            os.path.expanduser('~/.sitesearcher/index'), indexname=domain)
    except (EmptyIndexError, OSError):
        click.echo("""
            No index was found for domain {0}.
            Use "sitesearcher indexer {0}" to create one and try again.
        """.format(domain), err=True)

        return
    searchterm = click.prompt('Please enter your search')
    parser = QueryParser("content", schema=ix.schema)
    with ix.searcher() as searcher:
        pagenum = 1
        # Paging for search results
        while pagenum > 0:
            results = searcher.search_page(parser.parse(searchterm), pagenum)
            results.results.formatter = ConsoleFormatter()
            if results.results.is_empty():
                click.echo("No results found!")
            else:
                click.echo("Search results:")
                click.echo()
            # Output all results for current page in nice readable format
            for result in results:
                click.echo("Result #{}".format(result.rank + 1))
                click.echo("URL: {}".format(result['url']))
                # As the site content is not stored locally
                # send a request to get the content of the search result url
                request = Request(
                    result['url'],
                    headers={'User-Agent': get_user_agent()}
                )
                response = urlopen(request).read()
                click.echo("Extract:")
                content = clean_response_body(response)
                # Provide console color highlighting for result
                snippet = result.highlights("content", text=content)
                snippet_parts = re.split(
                    '(<searchphrase>.*?</searchphrase>)',
                    snippet,
                    re.DOTALL
                )
                for snippet_part in snippet_parts:
                    if snippet_part.startswith('<searchphrase>'):
                        searchphrase = re.search(
                            '<searchphrase>(.*?)</searchphrase>',
                            snippet_part,
                            re.DOTALL
                        ).group(1)
                        click.echo(
                            click.style(searchphrase, fg='blue', bold=True),
                            nl=False
                        )
                    else:
                        click.echo(snippet_part, nl=False)
                click.echo('\n')
            # Handle pagination
            if results.pagenum < results.pagecount:
                click.echo(
                    'Press any key to see next result page or <ESC> to abort',
                    nl=False
                )
                char = click.getchar()
                click.echo()
                if char != u'\x1b':
                    pagenum += 1
                    continue
            pagenum = -1


if __name__ == '__main__':
    sitesearcher()
