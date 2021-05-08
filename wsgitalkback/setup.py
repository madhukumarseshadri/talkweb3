from setuptools import setup

setup(
    name = 'wsgitalkback',
    version = '1.2',
    license = 'MIT License',
    url = 'http://www.github.com/madhukumarseshadri',
    description = "A responder framework to write responders to url requests, implements RFC 2616,RFC 2965",
    long_description = "A responder framework to write responders to url requests, implements RFC 2616,RFC 2965",
    author = 'Madhukumar Seshadri',
    author_email = 'madhukumarseshadri@gmail.com',
    zip_safe = False,
    platforms = 'any',
    packages = [
	    'wsgitalkback',
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
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
