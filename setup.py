import os
from setuptools import setup, find_packages


setup(
    name="django-slugmeta",
    version="0.1",
    author="Magnus Hult",
    author_email="magnus@magnushult.se",
    description="Slugmeta is a metaclass for translatable slugs for use together with django-transmeta",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
    ],
    url='http://github.com/hult/django-slugmeta',
    packages=find_packages('.')
)
