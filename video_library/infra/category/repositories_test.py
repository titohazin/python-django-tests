import copy
import random
from random import shuffle
import unittest

from django.conf import settings

from .repositories import CategoryRepositoryFactory, CategoryInMemoryRepository
from category.repositories import CategoryRepository
from category.entities import Category


class CategorySearchableInMemoryRepositoryUnitTests(unittest.TestCase):

    repo: CategoryInMemoryRepository

    def setUp(self) -> None:
        # Required configuration for integration tests (Django)
        if not settings.configured:
            settings.configure(USE_I18N=False)
        self.repo = CategoryRepositoryFactory.instance()

    def test_if_factory_return_a_category_repository_instance(self):
        self.assertIsInstance(self.repo, CategoryRepository)

    def test_category_sortable_fields(self):
        self.assertEqual(
            self.repo.sortable_fields,
            [
                'name',
                'description',
                'created_at',
                'updated_at',
                'is_active',
            ]
        )

    def test_apply_filter(self):
        variation = random.sample(range(15), 15)
        categories = [Category(
            name=f"cat_{i}", description=f"desc_{i}") for i in variation]
        categories_filtered = self.repo._apply_filter(categories, None)
        self.assertEqual(categories_filtered, categories)
        categories_filtered = self.repo._apply_filter(categories, '')
        self.assertEqual(categories_filtered, categories)
        categories_filtered = self.repo._apply_filter(categories, 'fake')
        self.assertEqual(categories_filtered, [])
        categories_filtered = self.repo._apply_filter(categories, 't_1')
        self.assertEqual(len(categories_filtered), 6)

    def test_apply_sort(self):
        variation = random.sample(range(5), 5)
        categories_source = [Category(
            name=f"cat_{i}", description=f"desc_{i}") for i in variation]
        categories_copy = copy.copy(categories_source)
        shuffle(categories_copy)
        categories_sorted = self.repo._apply_sort(categories_copy)
        self.assertEqual(categories_sorted, categories_source)
        categories_sorted = self.repo._apply_sort(categories_copy, None)
        self.assertEqual(categories_sorted, categories_source)
        categories_sorted = self.repo._apply_sort(categories_copy, 'fake_prop')
        self.assertEqual(categories_sorted, categories_source)
