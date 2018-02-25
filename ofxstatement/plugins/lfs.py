# -*- coding: utf-8 -*-

import re
import itertools
import logging
import locale
import os

from xlrd import open_workbook

from contextlib import contextmanager
from ofxstatement.parser import StatementParser
from ofxstatement.plugin import Plugin
from ofxstatement.statement import Statement, StatementLine, generate_transaction_id


def take(n, iterable):
    """Return first n items of the iterable as a list."""
    return list(itertools.islice(iterable, n))


@contextmanager
def scoped_setlocale(category, loc=None):
    """Scoped version of locale.setlocale()"""
    orig = locale.getlocale(category)
    try:
        yield locale.setlocale(category, loc)
    finally:
        locale.setlocale(category, orig)


def atof(string, loc=None):
    """Locale aware atof function for our parser."""
    with scoped_setlocale(locale.LC_NUMERIC, loc):
        return locale.atof(string)


class LfsStatementParser(StatementParser):
    date_format = '%Y-%m-%d'

    footer_regexps = [
        '^Datum:  -',
        '^Datum: ([0-9]{4}-[0-9]{2}-[0-9]{2}) - ([0-9]{4}-[0-9]{2}-[0-9]{2})$'
    ]

    def __init__(self, fin, locale=None, account_id=None, bank_id=None, currency_id=None):
        """
        Create a new LfsStatementParser instance.

        :param fin: filename to create parser for
        """
        
        if account_id is None:
            account_id = input("Account ID:")
        assert account_id

        if bank_id is None:
            bank_id = input("Bank ID:")
        assert bank_id

        if currency_id is None:
            currency_id = input("Currency ID:")
        assert currency_id

        self.locale = locale
        self.account_id = account_id
        self.bank_id = bank_id
        self.currency_id = currency_id

        self.workbook = open_workbook(filename=fin)
        self.sheet = self.workbook.sheet_by_index(0)
        self.validate()

        self.statement = self.parse_statement()

    def validate(self):
        """
        Naive validation to make sure that the document is structured the way it was
        when this parser was written.

        :raises ValueError if workbook has invalid format
        """

        try:
            self._validate()
        except AssertionError as e:
            raise ValueError(e)

    def parse_float(self, value):
        if isinstance(value, float):
            return value
        return atof(value, self.locale)

    def _validate(self):
        logging.info('Verifying file structure.')

        rows = list(self.sheet.get_rows())

        logging.info('Verifying that at least 2 rows.')
        assert len(rows) >= 2

        logging.info('Verifying that every row has 5 cells.')
        assert type(rows) == list
        for row in rows:
            assert len(row) == 5

        logging.info('Verifying that every cell has a value.')
        rows = [[c.value for c in row] for row in rows]

        logging.info('Verifying that first row is info header.')
        info_header_row = rows[0]
        assert info_header_row[0].startswith('Kontoutdrag')

        logging.info('Verifying that second row is statements header.')
        statement_header_row = rows[1]
        assert ['Bokf.dat', 'Trans.dat', 'Text', 'Insï¿½ttning/Uttag', 'Behï¿½llning'] == statement_header_row

        logging.info('Verified file structure - OK!')

    def sheet_rows(self):
        return [[c.value for c in row] for row in self.sheet.get_rows()]

    def parse_statement(self):
        statement = Statement()

        statement.account_id = self.account_id
        statement.bank_id = self.bank_id
        statement.currency = self.currency_id

        rows = self.sheet_rows()
        for r in rows[2:]:
            bokf_date, _, _, _, balance = r

            # first row will be our start balance & date
            first_row = (statement.start_date is None) or (statement.start_balance is None)
            if first_row:
                statement.start_date = self.parse_datetime(bokf_date)
                statement.start_balance = self.parse_float(balance)

            # last row will be our end balance & date
            statement.end_balance = self.parse_float(balance)
            statement.end_date = self.parse_datetime(bokf_date)

        #
        # Use the fact that first cell contains the statement date as a suffix e.g. 'Kontoutdrag - 2018-01-04'
        #
        info_header_row = rows[0]
        m = re.match('Kontoutdrag *- *([0-9]{4}-[0-9]{2}-[0-9]{2})$', info_header_row[0])
        if m:
            stmt_date, = m.groups()
            statement.end_date = self.parse_datetime(stmt_date)

        return statement

    def split_records(self):
        rows = self.sheet_rows()

        # Skip first 2 rows. Headers they are.
        for row in itertools.islice(rows, 2, None):
            yield row

    def parse_record(self, row):
        stmt_line = StatementLine()
        stmt_line.date = self.parse_datetime(row[0])
        stmt_line.date_user = self.parse_datetime(row[1])
        stmt_line.memo = row[2]
        stmt_line.amount = self.parse_float(row[3])
        stmt_line.id = generate_transaction_id(stmt_line)
        return stmt_line


def parse_bool(value):
    if value in ('True', 'true', '1'):
        return True
    if value in ('False', 'false', '0'):
        return False
    raise ValueError("Can't parse boolean value: %s" % value)


class LfsPlugin(Plugin):
    def get_parser(self, fin):
        # defaults
        kwargs = {
            'locale': 'sv_SE',
            'account_id': None,
            'bank_id': 'LFS',
            'currency_id': 'SEK',
        }

        # overwrite from settings
        if self.settings:
            if 'locale' in self.settings:
                kwargs['locale'] = parse_bool(self.settings.get('locale'))
            if 'account_id' in self.settings:
                kwargs['account_id'] = self.settings.get('account_id')
            if 'bank_id' in self.settings:
                kwargs['bank_id'] = self.settings.get('bank_id')
            if 'currency_id' in self.settings:
                kwargs['currency_id'] = self.settings.get('currency_id')

        # overwrite from env
        for k, v in kwargs.items():
            k2 = 'OFX_%s' % k.upper()
            kwargs[k] = os.getenv(k2, v)

        return LfsStatementParser(fin, **kwargs)
