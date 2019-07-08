import codecs
import csv
from datetime import datetime
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


def _format_iban(iban):
    return re.sub(r'\s+', '', iban, flags=re.UNICODE)


def _format_number_de(value: str) -> Decimal:
    thousands_sep = '.'
    decimal_sep = ','

    return Decimal(value.replace(thousands_sep, '').replace(decimal_sep, '.'))


class ECImporter(importer.ImporterProtocol):
    def __init__(
        self, iban, account, currency='EUR', file_encoding='utf-8-sig'
    ):
        self.iban = _format_iban(iban)
        self.account = account
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

        with open(file_.name, encoding=self.file_encoding) as fd:
            reader = csv.DictReader(
                fd, delimiter=';', quoting=csv.QUOTE_MINIMAL, quotechar='"'
            )

            for index, line in enumerate(reader):
                meta = data.new_metadata(file_.name, index)

                amount = Amount(
                    _format_number_de(line['Betrag']), line['Währung']
                )
                date = datetime.strptime(
                    line['Buchungstag'], '%d.%m.%Y'
                ).date()
                description = line['Buchungstext']
                payee = None

                postings = [
                    data.Posting(self.account, amount, None, None, None, None)
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
