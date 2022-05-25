import unittest
from datetime import datetime

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
        self.assertIsInstance(
            CategoryValidatorFactory.instance(), CategoryValidator)

    def test_if_invalidate_when_pass_no_dict_parameter(self):
        test_data = [[], 'foobar', False, 9]
        for data in test_data:
            msg = f'Fail with data: {data}'
            self.assertFalse(self.validator.validate(data), msg=msg)
            self.assertIsNotNone(self.validator.fields_errs, msg=msg)

    def test_valid_cases_for_name_field(self):
        test_data = [
            {'name': 'foobar'},
            {'name': 'f' * 3},
            {'name': 'f' * 255}
        ]
        for data in test_data:
            msg = f'Fail with data: {data}'
            self.assertTrue(self.validator.validate(data), msg=msg)
            self.assertIsNone(self.validator.fields_errs, msg=msg)
            self.assertEqual(self.validator.validated_data, data, msg=msg)

    def test_invalid_cases_for_name_field(self):
        test_data = [
            None, {}, {'name': None}, {'name': ''},
            {'name': 'f' * 2}, {'name': 'f' * 256},
            {'name': 5}, {'name': False},
            {'name': {}}, {'name': []}
        ]
        for data in test_data:
            msg = f'Fail with data: {data}'
            self.assertFalse(self.validator.validate(data), msg=msg)
            self.assertIsNotNone(self.validator.fields_errs, msg=msg)
            self.assertIsNotNone(self.validator.fields_errs['name'], msg=msg)

    def test_valid_cases_for_description_field(self):
        test_data = [
            {'name': 'foobar'},
            {'name': 'foobar', 'description': None},
            {'name': 'foobar', 'description': ''},
            {'name': 'foobar', 'description': 'foobar'},
            {'name': 'foobar', 'description': 'f' * 255}
        ]
        for data in test_data:
            msg = f'Fail with data: {data}'
            self.assertTrue(self.validator.validate(data), msg=msg)
            self.assertIsNone(self.validator.fields_errs, msg=msg)
            self.assertEqual(self.validator.validated_data, data, msg=msg)

    def test_invalid_cases_for_description_field(self):
        test_data = [
            {'description': 'f' * 256},
            {'description': 5}, {'description': False},
            {'description': {}}, {'description': []}
        ]
        for data in test_data:
            msg = f'Fail with data: {data}'
            self.assertFalse(self.validator.validate(data), msg=msg)
            self.assertIsNotNone(self.validator.fields_errs, msg=msg)
            self.assertIsNotNone(
                self.validator.fields_errs['description'], msg=msg)

    def test_valid_cases_for_is_active_field(self):
        test_data = [
            {'name': 'foobar'},
            {'name': 'foobar', 'is_active': True},
            {'name': 'foobar', 'is_active': False}
        ]
        for data in test_data:
            msg = f'Fail with data: {data}'
            self.assertTrue(self.validator.validate(data), msg=msg)
            self.assertIsNone(self.validator.fields_errs, msg=msg)
            self.assertEqual(self.validator.validated_data, data, msg=msg)

    def test_invalid_cases_for_is_active_field(self):
        test_data = [
            {'is_active': None}, {'is_active': 'foobar'},
            {'is_active': 0},  {'is_active': 1},
            {'is_active': '0'},  {'is_active': '1'},
            {'is_active': 9}, {'is_active': {}}, {'is_active': []}
        ]
        for data in test_data:
            msg = f'Fail with data: {data}'
            self.assertFalse(self.validator.validate(data), msg=msg)
            self.assertIsNotNone(self.validator.fields_errs, msg=msg)
            self.assertIsNotNone(
                self.validator.fields_errs['is_active'], msg=msg)

    def test_valid_cases_for_created_at_field(self):
        test_data = [
            {'name': 'foobar'},
            {'name': 'foobar', 'created_at': datetime.now()}
        ]
        for data in test_data:
            msg = f'Fail with data: {data}'
            self.assertTrue(self.validator.validate(data), msg=msg)
            self.assertIsNone(self.validator.fields_errs, msg=msg)
            self.assertEqual(self.validator.validated_data, data, msg=msg)

    def test_invalid_cases_for_created_at_field(self):
        test_data = [
            {'created_at': None}, {'created_at': 'foobar'},
            {'created_at': 9}, {'created_at': {}}, {'created_at': []}
        ]
        for data in test_data:
            msg = f'Fail with data: {data}'
            self.assertFalse(self.validator.validate(data), msg=msg)
            self.assertIsNotNone(self.validator.fields_errs, msg=msg)
            self.assertIsNotNone(
                self.validator.fields_errs['created_at'], msg=msg)

    def test_valid_cases_for_updated_at_field(self):
        test_data = [
            {'name': 'foobar'},
            {'name': 'foobar', 'updated_at': None},
            {'name': 'foobar', 'updated_at': datetime.now()}
        ]
        for data in test_data:
            msg = f'Fail with data: {data}'
            self.assertTrue(self.validator.validate(data), msg=msg)
            self.assertIsNone(self.validator.fields_errs, msg=msg)
            self.assertEqual(self.validator.validated_data, data, msg=msg)

    def test_invalid_cases_for_updated_at_field(self):
        test_data = [
            {'updated_at': 'foobar'},
            {'updated_at': 9}, {'updated_at': {}}, {'updated_at': []}
        ]
        for data in test_data:
            msg = f'Fail with data: {data}'
            self.assertFalse(self.validator.validate(data), msg=msg)
            self.assertIsNotNone(self.validator.fields_errs, msg=msg)
            self.assertIsNotNone(
                self.validator.fields_errs['updated_at'], msg=msg)
