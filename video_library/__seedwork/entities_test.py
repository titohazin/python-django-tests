from abc import ABC
from dataclasses import dataclass, is_dataclass
import unittest
import uuid

from __seedwork.entities import GenericEntity
from __seedwork.value_objects import UniqueEntityId


@dataclass(frozen=True, kw_only=True)
class GenericEntityStub(GenericEntity):
    prop: str = 'value'


class GenericEntityUnitTest(unittest.TestCase):

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
        prop_test = 'value'
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
        # Arrange:
        uuid_test = uuid.uuid4()
        prop_test = 'value'
        # Act:
        entity = GenericEntityStub(unique_entity_id=uuid_test, prop=prop_test)
        # Assert:
        self.assertDictEqual(entity.to_dict(), {
            'id': str(uuid_test),
            'prop': prop_test
        })

    # def test_convert_to_string(self):
        #     # Arrange/Act:
    #     value_object_1 = TestStubOneProperty()
    #     value_object_2 = TestStubTwoProperty()
    #     # Assert:
    #     self.assertEqual(str(value_object_1), value_object_1.prop)
    #     self.assertEqual(
    #         str(value_object_2),
    #         '{"prop": "prop value", "prop_": "other prop value"}'
    #     )
