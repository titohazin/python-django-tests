from dataclasses import FrozenInstanceError, is_dataclass
from datetime import datetime
from category.category import Category
import unittest


class CategoryUnitTest(unittest.TestCase):

    def test_if_is_a_data_class(self):
        # Arrange:
        is_category_dataclass = False
        # Act:
        is_category_dataclass = is_dataclass(Category)
        # Assert:
        self.assertTrue(is_category_dataclass)

    def test_constructor(self):
        # Arrange:
        data = {
            'name': 'movie_name',
            'description': 'desc',
            'is_active': True,
            'created_at': datetime.now()
        }
        # Act:
        category = Category(**data)
        # Assert:
        self.assertEqual(category.name, data['name'])
        self.assertEqual(category.description, data['description'])
        self.assertEqual(category.is_active, data['is_active'])
        self.assertEqual(category.created_at, data['created_at'])

    def test_constructor_default_values(self):
        # Act:
        category = Category(name='movie_name')
        # Assert:
        self.assertEqual(category.name, 'movie_name')
        self.assertEqual(category.description, None)
        self.assertEqual(category.is_active, True)
        self.assertIsInstance(category.created_at, datetime)

    def test_if_created_at_is_generated_correctly(self):
        # Act:
        category_1 = Category(name='cat1')
        category_2 = Category(name='cat2')
        # Assert:
        self.assertNotEqual(category_1.created_at, category_2.created_at)

    def test_if_is_immutable(self):
        # Arrange/Act/Assert:
        with self.assertRaises(FrozenInstanceError):
            unique_id_entity = Category(name='movie_name')
            unique_id_entity.name = 'other_name'
