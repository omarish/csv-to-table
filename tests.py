import pytest
from guesser import *


class TestTypeGuesser:

    def eq(self, result, answer):
        assert result == answer

    @pytest.fixture
    def get_is_boolean(self):
        for test, result in [
            ('true', True),
            ('ttrue', False),
            ('false', True),
            ('ffalse', False),
            ('0', True),
            ('1', True),
            ('2', False),
            ('T', True),
            ('F', True),
            ('t', True),
            ('f', True),
            ('z', False)
            ]:
            yield test, result

    def test_is_bool(self):
        for val, result in self.get_is_boolean():
            yield self.eq, is_boolean(val), result

    # TODO: test coverage for remaining functions.

class TestProcessor:
    def test_small(self):
        with open('tests/small.csv', 'rU') as f:
            proc = Processor(f)
            proc.process_csv()
            types = proc.determine_row_types()
            assert types == ['integer', 'boolean', 'string', 'date']
