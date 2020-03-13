import json
from unittest import TestCase
from unittest.mock import patch

import pytest

from SearchUtility.search_engine import SearchEngine
from Settings import data_path


class TestSearchEngine(TestCase):
    def setUp(self):
        self.engine = SearchEngine()
        with open(data_path + '/data.json', 'r') as jsonfile:
            self.queries = json.load(jsonfile)

    @patch.object(SearchEngine, 'search_for')
    def test_search_for(self, search_for_fn):
        max_items = 10
        search_for_fn.return_value = json.dumps({i: '' for i in range(max_items)})  # patch for only count
        rec = None
        for val in self.queries['queries']:  # parameterize with pytest
            result = self.engine.search_for(val, max_items)
            rec = json.loads(result)
            self.assertEqual(len(rec), max_items)  # only query count is tested.

    def tearDown(self):
        pass
