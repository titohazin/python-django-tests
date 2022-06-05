import datetime
import unittest

from django.conf import settings

from .entities import Category
from .dto import CategoryOutput, CategoryOutputMapper


class CategoryOutputUnitTests(unittest.TestCase):

    def test_output_inner_class(self):
        self.assertEqual(
            CategoryOutput.__annotations__,
            {
                'id_': str,
                'name': str,
                'description': str,
                'is_active': bool,
                'created_at': datetime,
                'updated_at': datetime,
            }
        )


class CategoryOutputStub(CategoryOutput):
    pass


class CategoryOutputMapperUnitTests(unittest.TestCase):

    def setUp(self) -> None:
        # Required configuration for integration tests (Django)
        if not settings.configured:
            settings.configure(USE_I18N=False)

    def test_from_child(self):
        mapper = CategoryOutputMapper.from_child(CategoryOutputStub)
        self.assertIsInstance(
            mapper.to_output(Category(name='foobar')),
            CategoryOutputStub
        )
        self.assertTrue(issubclass(
            mapper._CategoryOutputMapper__child, CategoryOutput))

    def test_from_default_child(self):
        mapper = CategoryOutputMapper.from_default_child()
        self.assertIsInstance(
            mapper.to_output(Category(name='foobar')),
            CategoryOutput
        )
        self.assertTrue(issubclass(
            mapper._CategoryOutputMapper__child, CategoryOutput))

    def test_if_convert_category_to_output(self):
        new_category = Category(name='foobar')
        self.assertEqual(
            CategoryOutputMapper.from_default_child().to_output(new_category),
            CategoryOutput(
                id_=new_category.id,
                name=new_category.name,
                description=new_category.description,
                is_active=new_category.is_active,
                created_at=new_category.created_at,
                updated_at=new_category.updated_at
            )
        )
