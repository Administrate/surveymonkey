#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'furl==2.1.3',
]

test_requirements = [
    'pytest==6.2.5',
    'validators==0.20.0'
]

setup(
    name='surveymonkey',
    version='1.0.0',
    description="Python wrapper for the Survey Monkey v3 API",
    long_description=readme,
    author="Aaron Bassett",
    author_email='engineering@getadministrate.com',
    url='https://github.com/Administrate/surveymonkey',
    packages=[
        'surveymonkey',
        'surveymonkey.collectors',
        'surveymonkey.responses',
        'surveymonkey.webhooks',
        'surveymonkey.messages'
    ],
    package_dir={'surveymonkey':
                 'surveymonkey'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='surveymonkey',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
