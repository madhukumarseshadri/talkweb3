"""
    Copyright(c) 2022 Madhukumar Seshadri, All rights reserved.
"""
from setuptools import setup
import os

md_path = os.path.join(os.path.dirname(__file__),'README.md')
long_description=open(md_path).read()

setup(
    name = 'talkweb',
    version = '1.2',
    license = 'MIT License',
    url = 'https://www.github.com/madhukumarseshadri/talkweb3',
    description = "A html to object framework",
    long_description = long_description,
    author = 'Madhukumar Seshadri',
    author_email = 'madhukumarseshadri@gmail.com',
    zip_safe = False,
    platforms = 'any',
    packages = [
	    'talkweb',
    ],
    include_package_data=True,
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ]
)
