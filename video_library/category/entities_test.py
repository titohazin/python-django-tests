from dataclasses import FrozenInstanceError, is_dataclass
from datetime import datetime
from category.entities import Category
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

    def test_update_method(self):
        # Arrange:
        name_test = 'name'
        description_test = 'description'
        datetime_test = datetime.now()
        category = Category(
            name='initial name',
            created_at=datetime_test,
            updated_at=datetime_test)
        # Act:
        category.update(name=name_test, description=description_test)
        # Assert:
        self.assertEqual(category.name, name_test)
        self.assertEqual(category.description, description_test)
        self.assertEqual(category.created_at, datetime_test)
        self.assertNotEqual(category.updated_at, datetime_test)
