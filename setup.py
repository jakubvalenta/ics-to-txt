from codecs import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ics_to_txt',

    version='1.1.0',

    description='ICS to TXT',
    long_description=long_description,

    url='https://lab.saloun.cz/jakub/ics-to-txt',

    author='Jakub Valenta',
    author_email='jakub@jakubvalenta.cz',

    license='Apache Software License',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Communications',
        'Topic :: Office/Business :: News/Diary',
        'Topic :: Office/Business :: Scheduling',
        'Topic :: Text Processing',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='',

    packages=find_packages(),

    install_requires=[
        'ics',
        'tzlocal',
    ],

    entry_points={
        'console_scripts': [
            'ics-to-txt=ics_to_txt.ics_to_txt:main',
        ],
    },
)
