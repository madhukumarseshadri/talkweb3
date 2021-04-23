from setuptools import setup

setup(
    name = 'talkweb',
    version = '1.1',
    license = 'MIT License',
    url = 'http://www.github.com/madhukumarsehadri',
    description = "A html to cell framework",
    long_description = "A html to cell framework",
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
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
