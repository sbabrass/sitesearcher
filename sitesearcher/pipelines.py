# -*- coding: utf-8 -*-
import os
import click
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh import index
from whoosh.writing import AsyncWriter


schema = Schema(url=ID(stored=True, unique=True),
                content=TEXT,)


class SearchPipeline(object):
    cleanup = False

    def open_spider(self, spider):
        """ When opening spider, open or create index. """

        index_dir = os.path.expanduser('~/.sitesearcher/index')
        if not os.path.exists(index_dir):
            os.makedirs(index_dir)

        self.indexname = spider.allowed_domains[0]
        if index.exists_in(index_dir, indexname=self.indexname):
            self.index = index.open_dir(index_dir, indexname=self.indexname)
        else:
            self.index = index.create_in(
                index_dir,
                indexname=self.indexname,
                schema=schema,
            )
        self.writer = AsyncWriter(self.index)

    def process_item(self, item, spider):
        """ Add crawled item to index.

        Add items using ``update_document`` to delete any previously indexed
        versions and avoid duplicates
        """

        self.writer.update_document(
            url=item.get('url'), content=item.get('content'))

    def close_spider(self, spider):
        """ Close index writer on closing of spider an clean up.

        On closing, delete any previously indexed items that have not been
        updated in this crawl, as these are obviously no longer reachable sites.
        """

        with self.index.searcher() as searcher:
            for page in searcher.all_stored_fields():
                if page['url'] not in spider.state['update_list']:
                    self.writer.delete_by_term('url', page['url'])
        self.writer.commit()
