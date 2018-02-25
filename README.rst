.. image:: https://travis-ci.org/themalkolm/ofxstatement-lfs.svg?branch=master
    :target: https://travis-ci.org/themalkolm/ofxstatement-lfs

ofxstatement-lfs
================

This is a collection of parsers for proprietary statement formats, produced by
`Lansforsakringar`_. It parses ``Kontoutdrag.xls`` file exported from internet bank.

It is a plugin for `ofxstatement`_.

.. _Lansforsakringar: https://www.lansforsakringar.se
.. _ofxstatement: https://github.com/kedder/ofxstatement

It is possible to use this plugin as a docker container. Instructions are `here <./DOCKER.rst>`_.

Input
=====

Lansforsakringar doesn't export account id in the statement. This means you need to explicitly provide it during
parsing as otherwise you get a blank account id. You can either provide it via env variable ``OFX_ACCOUNT_ID`` or
it will be asked during parsing automatically.

Configuration
=============

You can change default configuration if you want, here are the defaults:

.. code-block::

    [lfs]
    plugin = lfs
    locale = sv_SE
    bank_id = LFS
    currency_id = SEK
