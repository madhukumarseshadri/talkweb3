from setuptools import setup

setup(
    name = 'talksql',
    version = '1.1',
    license = 'MIT License',
    url = 'https://www.github.com/madhukumarseshadri',
    description = "A wrapper for mysqlconnector",
    long_description = "A wrapper for mysqlconnector",
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
    ]
)
