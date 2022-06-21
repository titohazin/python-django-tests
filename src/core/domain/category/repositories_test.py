import unittest

from core.domain.__seedwork.repositories import SearchParams, SearchResult

from .repositories import CategoryRepository


class CategoryRepositoryUnitTests(unittest.TestCase):

    def test_if_implements_searchable_repository_interface(self):
        with self.assertRaises(TypeError) as assert_error:
            CategoryRepository()
        self.assertTrue(
            "Can't instantiate abstract class CategoryRepository with "
            in assert_error.exception.args[0])

    def test_if_search_params_implements_default_search_params(self):
        search_params = CategoryRepository.SearchParams()
        self.assertIsInstance(search_params, SearchParams)

    def test_if_search_result_implements_default_search_result(self):
        search_result = CategoryRepository.SearchResult(
            items=[], total=1, current_page=1, per_page=1)
        self.assertIsInstance(search_result, SearchResult)
