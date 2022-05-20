from abc import ABC
from dataclasses import dataclass, is_dataclass
from datetime import datetime
import unittest
import uuid

from .entities import GenericEntity
from .value_objects import UniqueEntityId


@dataclass(frozen=True, slots=True)
class GenericEntityStub(GenericEntity):
    prop: str = 'value'
    prop_: str = 'value_'


class GenericEntityUnitTests(unittest.TestCase):

    def test_if_is_a_data_class(self):
        # Arrange:
        is_a_dataclass = False
        # Act:
        is_a_dataclass = is_dataclass(GenericEntity)
        # Assert:
        self.assertTrue(is_a_dataclass)

    def test_if_is_a_abstract_class(self):
        # Arrange:
        generic_entity = GenericEntity()
        # Act/Assert:
        self.assertIsInstance(generic_entity, ABC)

    def test_init_properties_and_unique_entity_id(self):
        # Arrange:
        prop_test = 'any value'
        # Act:
        entity = GenericEntityStub(prop=prop_test)
        # Assert:
        self.assertEqual(entity.prop, prop_test)
        self.assertIsInstance(entity.unique_entity_id, UniqueEntityId)
        self.assertEqual(entity.unique_entity_id.id, entity.id)

    def test_if_accept_a_valid_uuid(self):
        # Arrange:
        uuid_test = uuid.uuid4()
        # Act:
        entity = GenericEntityStub(unique_entity_id=uuid_test)
        # Assert:
        self.assertEqual(entity.id, str(uuid_test))

    def test_to_dict_method(self):
        # Arrange/Act:
        entity = GenericEntityStub()
        # Assert:
        self.assertDictEqual(entity.to_dict(), {
            'id': entity.id,
            'prop': entity.prop,
            'prop_': entity.prop_,
            'is_active': entity.is_active,
            'updated_at': entity.updated_at,
            'created_at': entity.created_at
        })

    def test_deactivate_method(self):
        # Arrange:
        entity = GenericEntity()
        # Act:
        entity.deactivate()
        # Assert:
        self.assertFalse(entity.is_active)

    def test_activate_method(self):
        # Arrange:
        entity = GenericEntity(is_active=False)
        # Act:
        entity.activate()
        # Assert:
        self.assertTrue(entity.is_active)

    def test_set_attr_method(self):
        # Arrange:
        prop_test = 'any value'
        initial_datetime = datetime.now()
        entity_stub = GenericEntityStub(updated_at=initial_datetime)
        # Act:
        entity_stub._set_attr('prop', prop_test)
        # Assert:
        self.assertEqual(entity_stub.prop, prop_test)
        self.assertNotEqual(entity_stub.updated_at, initial_datetime)

    def test_set_attrs_dict_method(self):
        # Arrange:
        prop_test = 'any value'
        initial_datetime = datetime.now()
        entity_stub = GenericEntityStub(updated_at=initial_datetime)
        # Act:
        entity_stub._set_attrs_dict({'prop': prop_test, 'prop_': prop_test})
        # Assert:
        self.assertEqual(entity_stub.prop, prop_test)
        self.assertEqual(entity_stub.prop_, prop_test)
        self.assertNotEqual(entity_stub.updated_at, initial_datetime)
