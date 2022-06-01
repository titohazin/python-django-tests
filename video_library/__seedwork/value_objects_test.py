from abc import ABC
from dataclasses import dataclass, FrozenInstanceError, is_dataclass
from unittest.mock import patch
import uuid
import unittest

from .value_objects import GenericValueObject, UniqueEntityId
from .exceptions import InvalidUuidException


@dataclass(frozen=True, slots=True)
class VOOnePropertyStub(GenericValueObject):
    prop: str = 'value'


@dataclass(frozen=True, slots=True)
class VOTwoPropertiesStub(GenericValueObject):
    prop: str = 'value'
    prop_: str = 'other value'


class GenericValueObjectUnitTests(unittest.TestCase):

    def test_if_is_a_data_class(self):
        # Arrange:
        is_a_dataclass = False
        # Act:
        is_a_dataclass = is_dataclass(GenericValueObject)
        # Assert:
        self.assertTrue(is_a_dataclass)

    def test_if_is_a_abstract_class(self):
        # Arrange:
        generic_value_object = GenericValueObject()
        # Act/Assert:
        self.assertIsInstance(generic_value_object, ABC)

    def test_init_properties(self):
        # Arrange:
        prop = 'new value'
        prop_ = 'new other value'
        # Act:
        value_object_1 = VOOnePropertyStub(prop=prop)
        value_object_2 = VOTwoPropertiesStub(prop=prop, prop_=prop_)
        # Assert:
        self.assertEqual(value_object_1.prop, prop)
        self.assertEqual(value_object_2.prop, prop)
        self.assertEqual(value_object_2.prop_, prop_)

    def test_if_is_immutable(self):
        # Arrange/Act/Assert:
        with self.assertRaises(FrozenInstanceError):
            value_object_1 = VOOnePropertyStub()
            value_object_1.prop = 'new value'

    def test_convert_to_string(self):
        # Arrange/Act:
        value_object_1 = VOOnePropertyStub()
        value_object_2 = VOTwoPropertiesStub()
        # Assert:
        self.assertEqual(str(value_object_1), value_object_1.prop)
        self.assertEqual(
            str(value_object_2),
            '{"prop": "value", "prop_": "other value"}'
        )


class UniqueEntityIdUnitTests(unittest.TestCase):

    def test_if_is_a_data_class(self):
        # Arrange:
        is_a_dataclass = False
        # Act:
        is_a_dataclass = is_dataclass(UniqueEntityId)
        # Assert:
        self.assertTrue(is_a_dataclass)

    def test_constructor(self):
        # Arrange:
        uuid_test = uuid.uuid4()
        uuid_str_test = '12212083-be2f-4a8c-9011-164e5dd02481'
        # Act:
        unique_entity_id_1 = UniqueEntityId(uuid_test)
        unique_entity_id_2 = UniqueEntityId(uuid_str_test)
        # Assert:
        self.assertEqual(str(uuid_test), unique_entity_id_1.id_)
        self.assertEqual(uuid_str_test, unique_entity_id_2.id_)

    def test_auto_generate_uuid_is_valid(self):
        # Arrange:
        unique_entity_id = UniqueEntityId()
        assert_result = False
        # Act:
        try:
            uuid.UUID(unique_entity_id.id_)
            assert_result = True
        except Exception:
            assert_result = False
        # Assert:
        self.assertTrue(assert_result)

    def test_if_is_immutable(self):
        # Arrange/Act/Assert:
        with self.assertRaises(FrozenInstanceError):
            unique_entity_id = UniqueEntityId()
            unique_entity_id.id_ = str(uuid.uuid4())

    def test_if_validate_method_was_call_once(self):
        # Arrange:
        with patch.object(
            UniqueEntityId,
            '_UniqueEntityId__validate',
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate
        ) as mock_validate:
            # Act:
            UniqueEntityId()
            # Assert:
            mock_validate.assert_called_once()

    def test_if_throws_exception_when_uuid_is_invalid(self):
        # Arrange:
        error_message = ''
        # Act/Assert:
        with self.assertRaises(InvalidUuidException) as assert_error:
            UniqueEntityId('testing_invalid_id')
        error_message = assert_error.exception.args[0]
        # Assert:
        self.assertEqual(error_message, 'ID must be a valid UUID')
