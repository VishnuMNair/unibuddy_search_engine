import json
from unittest import TestCase
import pytest

from SearchUtility.search_engine import SearchEngine
from Settings import data_path


class TestSearchEngine(TestCase):
    def setUp(self):
        self.engine = SearchEngine()
        with open(data_path + '/data.json', 'r') as jsonfile:
            self.queries = json.load(jsonfile)

    def test_search_for(self):
        max_items = 10
        rec = None
        for val in self.queries['queries']:  # parameterize with pytest
            result = self.engine.search_for(val, max_items)
            rec = json.loads(result)
            self.assertEqual(len(rec),
                         max_items)  # only validating count as of now, need to prepare data for validating algo
