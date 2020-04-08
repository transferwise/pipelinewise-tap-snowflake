#!/usr/bin/env python

from setuptools import setup

with open('README.md') as f:
      long_description = f.read()

setup(name='pipelinewise-tap-snowflake',
      version='2.0.0',
      description='Singer.io tap for extracting data from Snowflake - PipelineWise compatible',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author="TransferWise",
      url='https://github.com/transferwise/pipelinewise-tap-snowflake',
      classifiers=[
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3 :: Only'
      ],
      py_modules=['tap_snowflake'],
      install_requires=[
            'pipelinewise-singer-python==1.*',
            'snowflake-connector-python==2.2.2',
            'backoff==1.8.0',
            'pendulum==1.2.0',
            'python-dateutil<2.8.1,>=2.1',
      ],
      extras_require={
          'test': [
            'nose==1.3.7',
            'pylint==2.4.4',
            'unify==0.5'
          ]
      },
      entry_points='''
          [console_scripts]
          tap-snowflake=tap_snowflake:main
      ''',
      packages=['tap_snowflake', 'tap_snowflake.sync_strategies'],
)
