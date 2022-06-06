import unittest

from .use_cases import GenericUseCase


class UseCaseTests(unittest.TestCase):

    def test_if_throw_exception_if_no_implementation(self):
        with self.assertRaises(TypeError) as assert_error:
            GenericUseCase()
        self.assertEqual(
            assert_error.exception.args[0],
            "Can't instantiate abstract class GenericUseCase " +  # noqa: W504
            "with abstract method __call__")
