from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ics_to_txt',

    version='1.0.0',

    description='ICS to TXT',
    long_description=long_description,

    url='https://lab.saloun.cz/jakub/ics-to-txt',

    author='Jakub Valenta',
    author_email='jakub@jakubvalenta.cz',

    license='Apache Software License',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Artistic Software',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
    ],

    keywords='',

    packages=find_packages(),

    install_requires=[
        'ics',
        'pytz',
    ],

    entry_points={
        'console_scripts': [
            'ics-to-txt=ics_to_txt.ics_to_txt:main',
        ],
    },
)