from dataclasses import is_dataclass
from unittest.mock import patch
import uuid
import unittest

from __seedwork.exceptions import InvalidUuidException
from __seedwork.value_objects import UniqueEntityId


class UniqueEntityIdUnitTest(unittest.TestCase):

    def test_if_is_a_data_class(self):
        # Arrange:
        is_uuid_dataclass = False
        # Act:
        is_uuid_dataclass = is_dataclass(UniqueEntityId)
        # Assert:
        self.assertTrue(is_uuid_dataclass)

    def test_constructor(self):
        # Arrange:
        uuid_test = uuid.uuid4()
        uuid_str_test = '12212083-be2f-4a8c-9011-164e5dd02481'
        # Act:
        unique_id_1 = UniqueEntityId(uuid_test)
        unique_id_2 = UniqueEntityId(uuid_str_test)
        # Assert:
        self.assertEqual(str(uuid_test), unique_id_1.id_)
        self.assertEqual(uuid_str_test, unique_id_2.id_)

    def test_auto_generate_uuid_is_valid(self):
        # Arrange:
        unique_id_entity = UniqueEntityId()
        assert_result = False
        # Act:
        try:
            uuid.UUID(unique_id_entity.id_)
            assert_result = True
        except Exception:
            assert_result = False
        # Assert:
        self.assertTrue(assert_result)

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
        # Act:
        with self.assertRaises(InvalidUuidException) as assert_error:
            UniqueEntityId('testing_invalid_id')
        error_message = assert_error.exception.args[0]
        # Assert:
        self.assertEqual(error_message, 'ID must be a valid UUID')
