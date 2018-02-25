#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from distutils.core import setup

version = '0.0.1'
with open('README.rst', encoding="utf-8") as f:
    long_description = f.read()

setup(name='ofxstatement-lfs',
      version=version,
      author='Alexander Krasnukhin',
      author_email='the.malkolm@gmail.com',
      url='https://github.com/themalkolm/ofxstatement-lfs',
      description=('ofxstatement plugins for Lansforsakringar'),
      long_description=long_description,
      license='MIT',
      keywords=['ofx', 'ofxstatement', 'lfs', 'lansforsakringar'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3',
          'Natural Language :: English',
          'Topic :: Office/Business :: Financial :: Accounting',
          'Topic :: Utilities',
          'Environment :: Console',
          'Operating System :: OS Independent'
      ],
      packages=['ofxstatement', 'ofxstatement.plugins'],
      namespace_packages=['ofxstatement', 'ofxstatement.plugins'],
      entry_points={
          'ofxstatement': ['lfs = ofxstatement.plugins.lfs:LfsPlugin']
      },
      install_requires=[
          'appdirs==1.4.3',
          'ofxstatement==0.6.1',
          'xlrd==1.1.0',
      ],
      test_suite='ofxstatement.plugins.tests',
      include_package_data=True,
      zip_safe=True
      )
