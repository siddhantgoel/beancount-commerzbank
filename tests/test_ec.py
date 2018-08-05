import os.path
from unittest import TestCase
from tempfile import gettempdir
from textwrap import dedent

from beancount_commerzbank import ECImporter
from beancount_commerzbank.ec import FIELDS


def path_for_temp_file(name):
    return os.path.join(gettempdir(), name)


def _format(string, kwargs):
    return dedent(string).format(**kwargs).lstrip().encode('utf-8')


HEADER = ';'.join('"{}"'.format(field) for field in FIELDS)


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
                {header};
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
