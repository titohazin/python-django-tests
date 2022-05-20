import unittest


from .validators import Validator
from .exceptions import ValidationException


class ValidatorsUnitTests(unittest.TestCase):

    def test_value_method(self):
        # Arrange:
        value_test = 'value'
        prop_test = 'prop'
        # Act:
        validator = Validator.rules(value_test, prop_test)
        # Assert:
        self.assertIsInstance(validator, Validator)
        self.assertEqual(validator.value, value_test)
        self.assertEqual(validator.prop, prop_test)

    def test_required_rule(self):
        # Arrange:
        valid_data = [
            {'value': 'any value', 'prop': 'prop'},
            {'value': 5, 'prop': 'prop'},
            {'value': 0, 'prop': 'prop'},
            {'value': False, 'prop': 'prop'}
        ]
        # Act/Assert:
        for data in valid_data:
            self.assertIsInstance(
                Validator.rules(data['value'], data['prop']).required(), Validator)

    def test_required_rule_exception(self):
        # Arrange:
        invalid_data = [
            {'value': None, 'prop': 'prop'},
            {'value': '', 'prop': 'other prop'}
        ]
        # Act/Assert:
        for data in invalid_data:
            msg = f'test fail with value "{data["value"]}", and prop "{data["prop"]}"'
            with self.assertRaises(ValidationException, msg=msg) as assert_error:
                Validator.rules(data['value'], data['prop']).required()
            self.assertEqual(f'{data["prop"]} is required', assert_error.exception.args[0])

    def test_string_rule(self):
        # Arrange:
        valid_data = [
            {'value': None, 'prop': 'prop'},
            {'value': '', 'prop': 'prop'},
            {'value': " ", 'prop': 'prop'},
            {'value': 'any value', 'prop': 'prop'}
        ]
        # Act/Assert:
        for data in valid_data:
            self.assertIsInstance(
                Validator.rules(data['value'], data['prop']).string(), Validator)

    def test_string_rule_exception(self):
        # Arrange:
        invalid_data = [
            {'value': 5, 'prop': 'prop'},
            {'value': True, 'prop': 'other prop'},
            {'value': {}, 'prop': 'other prop'}
        ]
        # Act/Assert:
        for data in invalid_data:
            msg = f'test fail with value "{data["value"]}", and prop "{data["prop"]}"'
            with self.assertRaises(ValidationException, msg=msg) as assert_error:
                Validator.rules(data['value'], data['prop']).string()
            self.assertEqual(f'{data["prop"]} must be a string',
                             assert_error.exception.args[0])

    def test_min_length_rule(self):
        # Arrange:
        valid_data = [
            {'value': None, 'prop': 'prop'},
            {'value': '   ', 'prop': 'prop'},
            {'value': 'any', 'prop': 'prop'}
        ]
        min_len = 3
        # Act/Assert:
        for data in valid_data:
            self.assertIsInstance(
                Validator.rules(data['value'], data['prop']).min_length(min_len), Validator)

    def test_min_length_exception(self):
        # Arrange:
        invalid_data = [
            {'value': '', 'prop': 'prop'},
            {'value': 'hi', 'prop': 'other prop'}
        ]
        min_len = 3
        # Act/Assert:
        for data in invalid_data:
            msg = f'test fail with value "{data["value"]}", and prop "{data["prop"]}"'
            with self.assertRaises(ValidationException, msg=msg) as assert_error:
                Validator.rules(data['value'], data['prop']).min_length(min_len)
            self.assertEqual(f'{data["prop"]} must be equal or greater than {min_len} characters',
                             assert_error.exception.args[0])

    def test_max_length_rule(self):
        # Arrange:
        valid_data = [
            {'value': None, 'prop': 'prop'},
            {'value': '', 'prop': 'prop'},
            {'value': '   ', 'prop': 'prop'},
            {'value': 'any', 'prop': 'prop'}
        ]
        max_len = 3
        # Act/Assert:
        for data in valid_data:
            self.assertIsInstance(
                Validator.rules(data['value'], data['prop']).max_length(max_len), Validator)

    def test_max_length_exception(self):
        # Arrange:
        invalid_data = [
            {'value': '    ', 'prop': 'prop'},
            {'value': 'any value', 'prop': 'other prop'}
        ]
        max_len = 3
        # Act/Assert:
        for data in invalid_data:
            msg = f'test fail with value "{data["value"]}", and prop "{data["prop"]}"'
            with self.assertRaises(ValidationException, msg=msg) as assert_error:
                Validator.rules(
                    data['value'], data['prop']).max_length(max_len)
            self.assertEqual(f'{data["prop"]} must be equal or less than {max_len} characters',
                             assert_error.exception.args[0])

    def test_boolean_rule(self):
        # Arrange:
        valid_data = [
            {'value': None, 'prop': 'prop'},
            {'value': True, 'prop': 'prop'},
            {'value': False, 'prop': 'prop'}
        ]
        # Act/Assert:
        for data in valid_data:
            self.assertIsInstance(
                Validator.rules(data['value'], data['prop']).boolean(), Validator)

    def test_boolean_exception(self):
        # Arrange:
        invalid_data = [
            {'value': '', 'prop': 'prop'},
            {'value': 3, 'prop': 'other prop'},
            {'value': {}, 'prop': 'other prop'}
        ]
        # Act/Assert:
        for data in invalid_data:
            msg = f'test fail with value "{data["value"]}", and prop "{data["prop"]}"'
            with self.assertRaises(ValidationException, msg=msg) as assert_error:
                Validator.rules(data['value'], data['prop']).boolean()
            self.assertEqual(f'{data["prop"]} must be a boolean',
                             assert_error.exception.args[0])

    def test_valid_values_when_combinate_rules(self):
        # Arrange/Act/Assert:
        self.assertIsInstance(Validator.rules(
            'value', 'prop').required().string(), Validator)

        # Arrange/Act/Assert:
        self.assertIsInstance(Validator.rules(
            'value', 'prop').required().string().min_length(3), Validator)

        # Arrange/Act/Assert:
        self.assertIsInstance(Validator.rules(
            'value', 'prop').required().string().max_length(5), Validator)

        # Arrange/Act/Assert:
        self.assertIsInstance(Validator.rules(
            True, 'prop').required().boolean(), Validator)

    def test_throw_exception_when_combinate_rules_case_1(self):
        # Arrange/Act/Assert:
        with self.assertRaises(ValidationException) as assert_error:
            Validator.rules(None, 'prop').required(
            ).string().min_length(3).max_length(5)
        error_msg = assert_error.exception.args[0]
        self.assertEqual('prop is required', error_msg)

        # Arrange/Act/Assert:
        with self.assertRaises(ValidationException) as assert_error:
            Validator.rules(5, 'prop').required(
            ).string().min_length(3).max_length(5)
        error_msg = assert_error.exception.args[0]
        self.assertEqual('prop must be a string', error_msg)

    def test_throw_exception_when_combinate_rules_case_2(self):
        # Arrange/Act/Assert:
        with self.assertRaises(ValidationException) as assert_error:
            Validator.rules('hi', 'prop').required(
            ).string().min_length(3).max_length(5)
        error_msg = assert_error.exception.args[0]
        self.assertEqual(
            'prop must be equal or greater than 3 characters', error_msg)

        # Arrange/Act/Assert:
        with self.assertRaises(ValidationException) as assert_error:
            Validator.rules('any value', 'prop').required(
            ).string().min_length(3).max_length(5)
        error_msg = assert_error.exception.args[0]
        self.assertEqual(
            'prop must be equal or less than 5 characters', error_msg)

    def test_throw_exception_when_combinate_rules_case_3(self):
        # Arrange/Act/Assert:
        with self.assertRaises(ValidationException) as assert_error:
            Validator.rules(None, 'prop').required().boolean()
        error_msg = assert_error.exception.args[0]
        self.assertEqual('prop is required', error_msg)

        # Arrange/Act/Assert:
        with self.assertRaises(ValidationException) as assert_error:
            Validator.rules('any value', 'prop').required().boolean()
        error_msg = assert_error.exception.args[0]
        self.assertEqual('prop must be a boolean', error_msg)
