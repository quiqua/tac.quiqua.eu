# -*- coding: utf-8 -*-

from setuptools import setup

project = "tacsite"

setup(
    name=project,
    version='1.0',
    description='TAC Tournament Website.',
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
        'py-bcrypt'
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
