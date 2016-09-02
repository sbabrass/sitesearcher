import os
from setuptools import setup
from setuptools import find_packages

setup(
    name='SiteSearcher',
    version='0.1',
    description='A command line tool that creates fulltext search indexes of your favourite websites on your machine, and allows you to search them locally',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "License :: Repoze Public License",
    ],
    author="Sebastian Brass (sbabrass)",
    license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'scrapy',
        'whoosh',
        'pyasn1',
    ],
    entry_points='''
        [console_scripts]
        sitesearcher=sitesearcher.script:sitesearcher
    ''',
)
