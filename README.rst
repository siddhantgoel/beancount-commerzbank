Beancount Commerzbank Importer
==============================

:code:`beancount-commerzbank` provides an Importer for converting CSV exports of
Commerzbank_ account summaries to the Beancount_ format.

.. image:: https://github.com/siddhantgoel/beancount-commerzbank/workflows/beancount-commerzbank/badge.svg
    :target: https://github.com/siddhantgoel/beancount-commerzbank/workflows/beancount-commerzbank/badge.svg

.. image:: https://img.shields.io/pypi/v/beancount-commerzbank.svg
    :target: https://pypi.python.org/pypi/beancount-commerzbank

.. image:: https://img.shields.io/pypi/pyversions/beancount-commerzbank.svg
    :target: https://pypi.python.org/pypi/beancount-commerzbank

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

Installation
------------

.. code-block:: bash

    $ pip install beancount-commerzbank

In case you prefer installing from the Github repository, please note that
:code:`main` is the development branch so :code:`stable` is what you should be
installing from.

Usage
-----

.. code-block:: python

    from beancount_commerzbank import ECImporter

    CONFIG = [
        ECImporter(
            IBAN_NUMBER,
            'Assets:Commerzbank:EC',
            currency='EUR',
            file_encoding='utf-8-sig',
        ),
    ]

.. _Beancount: http://furius.ca/beancount/
.. _Commerzbank: https://www.commerzbank.de/
