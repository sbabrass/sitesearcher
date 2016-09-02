============
SiteSearcher
============

About SiteSearcher
==================

**SiteSearcher** is a command line tool that creates fulltext search indexes of your favourite websites on your machine, and allows you to search them locally.

Usage
-----

:code:`sitesearcher indexer <mydomain>` - Create a local search index for :code:`<mydomain>`

:code:`sitesearcher search <mydomain>` - Open search prompt for :code:`<mydomain>`

Indexing of large sites can take quite long, but you can stop the indexer at any time and continue later at the point where you left off. To halt the indexer, simply type :code:`<CTRL>+C` once and wait for graceful exit. To restart run the index command again with the :code:`--continue` flag, i.e. :code:`sitesearcher indexer <mydomain> --continue`.

Web Server Friendly
-------------------

**SiteSearcher** tries to be web server friendly, while crawling. It obeys :code:`robot.txt`, identifies itself with the :code:`"SiteSearcher"` UserAgent and uses the `Scrapy Autothrottle Extension <http://doc.scrapy.org/en/latest/topics/autothrottle.html>`_ to reduce the load on the server.

Installing SiteSearcher
=======================

If you have :code:`pip` installed, you can use :code:`pip` to download and install **SiteSearcher**.

.. code:: bash

	pip install sitesearcher

**SiteSearcher** uses the `Scrapy <http://scrapy.org>`_ bot framework and therefore inherits its `dependencies <http://doc.scrapy.org/en/latest/intro/install.html#installing-scrapy>`_.


Getting the source
==================

Download source releases from PyPI at http://pypi.python.org/pypi/sitesearcher

You can check out the latest version of source code from GitHub.

.. code::

	git clone https://github.com/sbabrass/sitesearcher

Python Version Support
======================

**SiteSearcher** supports Python Versions 2.7 and 3.3+.

However switching between Python versions may require a rebuild of your indexes, as there is currently no support for SiteSearcher/Python 2 to read and write indexes created with SiteSearcher/Python 3 and vice versa.
