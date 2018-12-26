import codecs
from contextlib import contextmanager
import csv
from datetime import datetime
import locale
import re

from beancount.core.amount import Amount
from beancount.core import data
from beancount.core.number import Decimal
from beancount.ingest import importer


FIELDS = (
    'Buchungstag',
    'Wertstellung',
    'Umsatzart',
    'Buchungstext',
    'Betrag',
    'Währung',
    'Auftraggeberkonto',
    'Bankleitzahl Auftraggeberkonto',
    'IBAN Auftraggeberkonto',
    'Kategorie',
)


@contextmanager
def _change_locale(key, value):
    original = locale.getlocale(key)

    try:
        locale.setlocale(key, value)
        yield
    finally:
        locale.setlocale(key, original)


def _format_iban(iban):
    return re.sub(r'\s+', '', iban, flags=re.UNICODE)


class ECImporter(importer.ImporterProtocol):
    def __init__(
        self,
        iban,
        account,
        currency='EUR',
        numeric_locale='de_DE.UTF-8',
        file_encoding='utf-8-sig',
    ):
        self.iban = _format_iban(iban)
        self.account = account
        self.numeric_locale = numeric_locale
        self.file_encoding = file_encoding

    def file_account(self, _):
        return self.account

    def identify(self, file_):
        with open(file_.name, encoding=self.file_encoding) as fd:
            try:
                line = (
                    fd.readline()
                    .strip()
                    .strip(codecs.BOM_UTF8.decode('utf-8'))
                )
            except UnicodeDecodeError:
                return False

            if not line:
                return False

            return line == ';'.join(FIELDS)

    def extract(self, file_):
        entries = []

        with _change_locale(locale.LC_NUMERIC, self.numeric_locale):
            with open(file_.name, encoding=self.file_encoding) as fd:
                reader = csv.DictReader(
                    fd, delimiter=';', quoting=csv.QUOTE_MINIMAL, quotechar='"'
                )

                for index, line in enumerate(reader):
                    meta = data.new_metadata(file_.name, index)

                    amount = Amount(
                        locale.atof(line['Betrag'], Decimal), line['Währung']
                    )
                    date = datetime.strptime(
                        line['Buchungstag'], '%d.%m.%Y'
                    ).date()
                    description = line['Buchungstext']
                    payee = None

                    postings = [
                        data.Posting(
                            self.account, amount, None, None, None, None
                        )
                    ]

                    entries.append(
                        data.Transaction(
                            meta,
                            date,
                            self.FLAG,
                            payee,
                            description,
                            data.EMPTY_SET,
                            data.EMPTY_SET,
                            postings,
                        )
                    )

            return entries
