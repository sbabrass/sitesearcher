import os
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
except IOError:
    README = ''
try:
    CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()
except IOError:
    CHANGES = ''

setup(
    name='sitesearcher',
    version='0.1a1',
    description='A command line tool that creates fulltext search '
                'indexes of your favourite websites on your machine, '
                'and allows you to search them locally',
    long_description='\n\n'.join([README, CHANGES]),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "License :: Repoze Public License",
    ],
    author="Sebastian Brass (sbabrass)",
    license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
    keywords='scrapy whoosh searching indexing websearch',
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
