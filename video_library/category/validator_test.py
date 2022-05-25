import unittest

from django.conf import settings

from category.validator import CategoryValidator, CategoryValidatorFactory


class CategoryValidatorUnitTest(unittest.TestCase):

    validator: CategoryValidator

    def setUp(self) -> None:
        # Required configuration for integration tests (Django)
        if not settings.configured:
            settings.configure(USE_I18N=False)

        self.validator = CategoryValidatorFactory.instance()
        return super().setUp()

    def test_if_factory_instances_a_category_validator(self):
        self.assertIsInstance(CategoryValidatorFactory.instance(), CategoryValidator)

    def test_invalid_cases_for_name_property(self):
        # Arrange/Act:
        is_valid = self.validator.validate(None)
        # Assert:
        self.assertFalse(is_valid)
        print(self.validator.fields_errs)
