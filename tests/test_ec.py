import datetime
import os.path
from unittest import TestCase
from tempfile import gettempdir
from textwrap import dedent

from beancount_commerzbank import ECImporter
from beancount_commerzbank.ec import FIELDS


def path_for_temp_file(name):
    return os.path.join(gettempdir(), name)


def _format(string, kwargs):
    return dedent(string).format(**kwargs).lstrip().encode('utf-8-sig')


HEADER = ';'.join(FIELDS)


class ECImporterTestCase(TestCase):
    def setUp(self):
        super(ECImporterTestCase, self).setUp()

        self.iban = 'DE99999999999999999999'
        self.filename = path_for_temp_file('{}.csv'.format(self.iban))

    def tearDown(self):
        if os.path.isfile(self.filename):
            os.remove(self.filename)

        super(ECImporterTestCase, self).tearDown()

    def test_identify_correct(self):
        importer = ECImporter(self.iban, 'Assets:Commerzbank:EC')

        with open(self.filename, 'wb') as fd:
            fd.write(_format('''
                {header}
            ''', dict(header=HEADER)))

        with open(self.filename) as fd:
            self.assertTrue(importer.identify(fd))

    def test_identify_invalid(self):
        importer = ECImporter(self.iban, 'Assets:Commerzbank:EC')

        with open(self.filename, 'wb') as fd:
            fd.write(_format('''
                lolno
            ''', {}))

        with open(self.filename) as fd:
            self.assertFalse(importer.identify(fd))

    def test_extract_empty(self):
        importer = ECImporter(self.iban, 'Assets:Commerzbank:EC')

        with open(self.filename, 'wb') as fd:
            fd.write(_format('''
                {header}
            ''', dict(header=HEADER)))

        with open(self.filename) as fd:
            self.assertFalse(importer.extract(fd))

    def test_extract(self):
        importer = ECImporter(self.iban, 'Assets:Commerzbank:EC')

        with open(self.filename, 'wb') as fd:
            fd.write(_format('''
                {header}

                15.07.2018;15.07.2018;Lastschrift;"PayPal Europe S.a.r.l.";-13,47;EUR;000000000;00000000;DE00000000000000000000;Unkategorisierte Ausgaben
                15.07.2018;15.07.2018;Gutschrift;"MAX MUSTERMANN End-to-End-Ref.: NOTPROVIDED Kundenreferenz: XXXX0000000000000000000000000000000";50,00;EUR;111111111;11111111;DE11111111111111111111;Unkategorisierte Ausgaben
            ''', dict(header=HEADER)))  # NOQA

        with open(self.filename) as fd:
            transactions = importer.extract(fd)

            self.assertEqual(len(transactions), 2)

            self.assertEqual(transactions[0].date, datetime.date(2018, 7, 15))
            self.assertEqual(transactions[0].payee, '000000000')
            self.assertEqual(transactions[0].narration,
                             'PayPal Europe S.a.r.l.')

            self.assertEqual(transactions[1].date, datetime.date(2018, 7, 15))
            self.assertEqual(transactions[1].payee, '111111111')
            self.assertEqual(transactions[1].narration,
                             ('MAX MUSTERMANN End-to-End-Ref.: NOTPROVIDED '
                              'Kundenreferenz: '
                              'XXXX0000000000000000000000000000000'))
