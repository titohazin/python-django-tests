from dataclasses import fields
import unittest
from unittest.mock import MagicMock, PropertyMock, patch

from rest_framework.serializers import Serializer
from rest_framework import serializers
from django.conf import settings

from .validators import FieldsValidatorInterface, DRFFieldsValidator
from .validators import DRFStrictCharField, DRFStrictBooleanField


class ValidatorFieldsInterfaceUnitTests(unittest.TestCase):

    def test_if_validate_method_is_abstract(self):
        with self.assertRaises(TypeError) as assert_error:
            FieldsValidatorInterface().validate()
        self.assertEqual(assert_error.exception.args[0], "Can't instantiate " +
                         "abstract class FieldsValidatorInterface with abstract method validate")

    def test_if_errors_field_meets_specifications(self):
        # sourcery skip: class-extract-method
        class_fields = fields(FieldsValidatorInterface)
        fields_errors_field = class_fields[0]
        self.assertEqual(fields_errors_field.name, 'fields_errors')
        self.assertIsNone(fields_errors_field.default)

    def test_if_data_field_meets_specifications(self):
        class_fields = fields(FieldsValidatorInterface)
        validated_data_field = class_fields[1]
        self.assertEqual(validated_data_field.name, 'validated_data')
        self.assertIsNone(validated_data_field.default)


class DRFValidatorFieldsUnitTests(unittest.TestCase):

    @patch.object(Serializer, 'is_valid', return_value=True)
    @patch.object(
        Serializer,
        'validated_data',
        new_callable=PropertyMock,
        return_value={'foo': 'bar'})
    def test_if_validator_validate_and_return_validated_data(
            self,
            mock_is_valid: MagicMock,
            mock_validated_data: PropertyMock):
        # Arrange:
        validator = DRFFieldsValidator()
        # Act:
        is_valid = validator.validate(Serializer())
        # Assert:
        self.assertTrue(is_valid)
        mock_is_valid.assert_called_once()
        self.assertEqual(validator.validated_data, {'foo': 'bar'})

    @patch.object(Serializer, 'is_valid', return_value=False)
    @patch.object(
        Serializer,
        'errors',
        new_callable=PropertyMock,
        return_value={'foobar': ['foo err', 'bar err']})
    def test_if_validator_not_validate_data_and_return_errors(
            self,
            mock_is_valid: MagicMock,
            mock_errors: PropertyMock):
        # Arrange:
        validator = DRFFieldsValidator()
        # Act:
        is_valid = validator.validate(Serializer())
        # Assert:
        self.assertFalse(is_valid)
        mock_is_valid.assert_called_once()
        self.assertEqual(validator.fields_errors, {'foobar': ['foo err', 'bar err']})


class SerializerStub(serializers.Serializer):
    foo = serializers.CharField()
    bar = serializers.IntegerField()


class DRFValidatorFieldsIntegrationTests(unittest.TestCase):

    def setUp(self):
        # Required configuration for integration tests (Django)
        if not settings.configured:
            settings.configure(USE_I18N=False)

    def test_validation_with_fields_errors(self):
        # Arrange:
        validator = DRFFieldsValidator()
        serializer = SerializerStub(data={})
        # Act:
        is_valid = validator.validate(serializer)
        # Assert:
        self.assertFalse(is_valid)
        self.assertEqual(validator.validated_data, None)
        self.assertDictEqual(
            validator.fields_errors,
            {
                'foo': ['This field is required.'],
                'bar': ['This field is required.']
            }
        )

    def test_validation_without_fields_errors(self):
        # Arrange:
        validator = DRFFieldsValidator()
        data = {'foo': 'value', 'bar': 0}
        serializer = SerializerStub(data=data)
        # Act:
        is_valid = validator.validate(serializer)
        # Assert:
        self.assertTrue(is_valid)
        self.assertEqual(validator.fields_errors, None)
        self.assertDictEqual(validator.validated_data, data)


class DRFStrictCharFieldUnitTests(unittest.TestCase):

    def setUp(self) -> None:
        # Required configuration for integration tests (Django)
        if not settings.configured:
            settings.configure(USE_I18N=False)

    def test_if_invalid_when_pass_none_as_data(self):
        # Arrange:
        class DRFStrictCharFieldSerializerStub(serializers.Serializer):
            foobar = DRFStrictCharField()

        # Arrange:
        serializer = DRFStrictCharFieldSerializerStub(data=None)
        # Act/Assert:
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.validated_data, {})
        self.assertEqual(serializer.errors['non_field_errors'][0].code, 'null')

    def test_if_invalid_when_not_str_value(self):
        # Arrange:
        class DRFStrictCharFieldSerializerStub(serializers.Serializer):
            foobar = DRFStrictCharField()

        test_data = [True, 9, {}, {'any value'}, [], ['any value']]
        for data in test_data:
            serializer = DRFStrictCharFieldSerializerStub(data={'foobar': data})
            # Act/Assert:
            self.assertFalse(serializer.is_valid())
            self.assertEqual(serializer.validated_data, {})
            self.assertEqual(serializer.errors['foobar'][0].code, 'invalid')

        # Arrange:
        serializer = DRFStrictCharFieldSerializerStub(data={'foobar': None})
        # Act/Assert:
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.validated_data, {})
        self.assertEqual(serializer.errors['foobar'][0].code, 'null')

    def test_if_valid_when_pass_a_str_value(self):
        # Arrange:
        class DRFStrictCharFieldSerializerStub(serializers.Serializer):
            foobar = DRFStrictCharField()

        test_data = {'foobar': 'valid value'}
        serializer = DRFStrictCharFieldSerializerStub(data=test_data)
        # Act/Assert:
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, test_data)
        self.assertEqual(serializer.errors, {})

    def test_if_valid_when_pass_a_null_value(self):
        # Arrange:
        class DRFStrictCharFieldSerializerStub(serializers.Serializer):
            foobar = DRFStrictCharField(required=False, allow_null=True)

        test_data = {'foobar': None}
        serializer = DRFStrictCharFieldSerializerStub(data=test_data)
        # Act/Assert:
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, test_data)
        self.assertEqual(serializer.errors, {})


class DRFStrictBooleanFieldUnitTests(unittest.TestCase):

    def setUp(self) -> None:
        # Required configuration for integration tests (Django)
        if not settings.configured:
            settings.configure(USE_I18N=False)

    def test_if_invalid_when_pass_none_as_data(self):
        # Arrange:
        class DRFStrictBooleanFieldSerializerStub(serializers.Serializer):
            foobar = DRFStrictBooleanField()

        # Arrange:
        serializer = DRFStrictBooleanFieldSerializerStub(data=None)
        # Act/Assert:
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.validated_data, {})
        self.assertEqual(serializer.errors['non_field_errors'][0].code, 'null')

    def test_if_invalid_when_not_boolean_value(self):
        # Arrange:
        class DRFStrictBooleanFieldSerializerStub(serializers.Serializer):
            foobar = DRFStrictBooleanField()

        test_data = [1, 0, "1", "0", "True", "False", 'value', {}]
        for data in test_data:
            serializer = DRFStrictBooleanFieldSerializerStub(
                data={'foobar': data})
            # Act/Assert:
            self.assertFalse(serializer.is_valid())
            self.assertEqual(serializer.validated_data, {})
            self.assertEqual(serializer.errors['foobar'][0].code, 'invalid')

        # Arrange:
        serializer = DRFStrictBooleanFieldSerializerStub(data={'foobar': None})
        # Act/Assert:
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.validated_data, {})
        self.assertEqual(serializer.errors['foobar'][0].code, 'null')

    def test_if_valid_when_pass_boolean_values(self):
        # Arrange:
        class DRFStrictBooleanFieldSerializerStub(serializers.Serializer):
            foobar = DRFStrictBooleanField()

        test_data = [True, False]
        for data in test_data:
            serializer = DRFStrictBooleanFieldSerializerStub(
                data={'foobar': data})
            # Act/Assert:
            self.assertTrue(serializer.is_valid())
            self.assertTrue(isinstance(
                serializer.validated_data['foobar'], bool))
            self.assertEqual(serializer.errors, {})

    def test_if_valid_when_pass_a_null_value_with_allow_null(self):
        # Arrange:
        class DRFStrictBooleanFieldSerializerStub(serializers.Serializer):
            foobar = DRFStrictBooleanField(required=False, allow_null=True)

        test_data = {'foobar': None}
        serializer = DRFStrictBooleanFieldSerializerStub(data=test_data)
        # Act/Assert:
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, test_data)
        self.assertEqual(serializer.errors, {})
