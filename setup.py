#!/usr/bin/env python

from setuptools import setup

with open('README.md') as f:
      long_description = f.read()

setup(name='pipelinewise-tap-snowflake',
      version='1.0.2',
      description='Singer.io tap for extracting data from Snowflake - PipelineWise compatible',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author="TransferWise",
      url='https://github.com/transferwise/pipelinewise-tap-postgres',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['tap_snowflake'],
      install_requires=[
          'singer-python==5.3.1',
          'snowflake-connector-python==1.7.4',
          'backoff==1.3.2',
          'pendulum==1.2.0'
      ],
      entry_points='''
          [console_scripts]
          tap-snowflake=tap_snowflake:main
      ''',
      packages=['tap_snowflake', 'tap_snowflake.sync_strategies'],
)
