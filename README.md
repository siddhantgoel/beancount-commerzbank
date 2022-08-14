## ⚠️ Looking for maintainers

This project is not being actively maintained.

It might still continue to work. But as I don't have a Commerzbank account
anymore, I don't know how the updated CSV format looks like and can't adjust
the Importer classes accordingly.

Drop me an email if you'd like to take ownership.

---

# Beancount Commerzbank Importer

`beancount-commerzbank` provides an Importer for converting CSV exports of
[Commerzbank] account summaries to the [Beancount] format.

[![image](https://github.com/siddhantgoel/beancount-commerzbank/workflows/beancount-commerzbank/badge.svg)](https://github.com/siddhantgoel/beancount-commerzbank/workflows/beancount-commerzbank/badge.svg)

[![image](https://img.shields.io/pypi/v/beancount-commerzbank.svg)](https://pypi.python.org/pypi/beancount-commerzbank)

[![image](https://img.shields.io/pypi/pyversions/beancount-commerzbank.svg)](https://pypi.python.org/pypi/beancount-commerzbank)

[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Installation

```bash
$ pip install beancount-commerzbank
```

In case you prefer installing from the Github repository, please note that
`main` is the development branch so `stable` is what you should be installing
from.

## Usage

```python
from beancount_commerzbank import ECImporter

CONFIG = [
    ECImporter(
        IBAN_NUMBER,
        'Assets:Commerzbank:EC',
        currency='EUR',
        file_encoding='utf-8-sig',
    ),
]
```

[Beancount]: http://furius.ca/beancount/
[Commerzbank]: https://www.commerzbank.de/
