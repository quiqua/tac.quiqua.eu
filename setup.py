# -*- coding: utf-8 -*-

from setuptools import setup

project = "tacsite"

setup(
    name=project,
    version='0.1',
    description='Fbone (Flask bone) is a Flask (Python microframework) template/bootstrap/boilerplate application.',
    author='Marcel Radischat',
    author_email='marcel@quiqua.eu',
    packages=["tacsite"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask>=0.10.1',
        'Flask-SQLAlchemy',
        'Flask-WTF',
        'Flask-Mail',
        'Flask-Security',
    ],
    #test_suite='tests',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries'
    ]
)
