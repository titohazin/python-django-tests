import unittest

from __seedwork.repositories import SearchParams, SearchResult

from .repositories import CategoryRepository


class CategoryRepositoryUnitTests(unittest.TestCase):

    def test_if_implements_searchable_repository_interface(self):
        with self.assertRaises(TypeError) as assert_error:
            CategoryRepository()
        self.assertEqual(
            assert_error.exception.args[0],
            "Can't instantiate abstract class CategoryRepository with " +
            "abstract methods delete, find_all, find_by_id, insert, search, update")

    def test_if_search_params_implements_default_search_params(self):
        search_params = CategoryRepository.SearchParams()
        self.assertIsInstance(search_params, SearchParams)

    def test_if_search_result_implements_default_search_result(self):
        search_result = CategoryRepository.SearchResult(
            items=[], total=1, current_page=1, per_page=1)
        self.assertIsInstance(search_result, SearchResult)
