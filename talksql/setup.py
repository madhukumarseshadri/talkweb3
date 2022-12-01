"""
    Copyright(c) 2022 Madhukumar Seshadri, All rights reserved.
"""
from setuptools import setup
import os

md_path = os.path.join(os.path.dirname(__file__),'README.md')
long_description=open(md_path).read()

setup(
    name = 'talksql',
    version = '1.2',
    license = 'MIT License',
    url = 'https://www.github.com/madhukumarseshadri/talkweb3',
    description = "A utility package for sql work",
    long_description = long_description,
    long_description_content_type="text/markdown",
    author = 'Madhukumar Seshadri',
    author_email = 'madhukumarseshadri@gmail.com',
    zip_safe = False,
    platforms = 'any',
    packages = [
	    'talksql',
    ],
    include_package_data=True,
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
    ]
)
