#!/usr/bin/env python
#encoding=utf-8
from distutils.core import setup
import sys

reload(sys).setdefaultencoding("UTF-8")


setup(
    name='retranslate',
    version='0.1',
    author='Andrey Beletsky',
    author_email='andrey@vr2.net',
    packages=[
        'retranslate'
    ],
    url='http://www.vr2.net',
    download_url = 'https://github.com/satels/django-qiwi/zipball/master',
    license = 'MIT license',
    description = 'A django app to translate non-english strings found in source code to english',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ),
    install_requires=['Django>=1.3', 'polib==1.0.2']
)
