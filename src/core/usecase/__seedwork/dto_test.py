from typing import List, Optional
import unittest

from core.domain.__seedwork.repositories import Filter, SearchResult

from .dto import SearchInput, SearchOutput, SearchOutputMapper, Item


class SearchInputUnitTests(unittest.TestCase):

    def test_input_inner_class(self):
        self.assertEqual(
            SearchInput.__annotations__,
            {
                'page': Optional[int],
                'per_page': Optional[int],
                'sort_by': Optional[str],
                'sort_dir': Optional[str],
                'filter_': Optional[Filter]
            }
        )


class SearchOutputUnitTests(unittest.TestCase):

    def test_output_inner_class(self):
        self.assertEqual(
            SearchOutput.__annotations__,
            {
                'items': List[Item],
                'total': int,
                'current_page': int,
                'per_page': int,
                'last_page': int
            }
        )


class SearchOutputWrapperUnitTests(unittest.TestCase):

    def test_from_child(self):
        mapper = SearchOutputMapper.from_child(SearchOutput)
        self.assertIsInstance(mapper, SearchOutputMapper)
        self.assertTrue(issubclass(
            mapper._SearchOutputMapper__child, SearchOutput))

    def test_to_output(self):
        result = SearchResult(
            items=['foobar'],
            total=1,
            current_page=1,
            per_page=1,
            sort_by=None,
            sort_dir=None,
            filter_=None
        )
        output_ = SearchOutputMapper.from_child(
            SearchOutput).to_output(result.items, result)
        self.assertEqual(
            output_,
            SearchOutput(
                items=result.items,
                total=result.total,
                current_page=result.current_page,
                last_page=result.last_page,
                per_page=result.per_page
            )
        )
