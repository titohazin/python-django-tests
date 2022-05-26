from dataclasses import dataclass
import unittest

from .entities import GenericEntity
from .repositories import InMemoryRepository, RepositoryInterface


class RepositoryInterfaceUnitTest(unittest.TestCase):

    def test_if_are_a_abstract_class_and_abstract_methods(self):
        with self.assertRaises(TypeError) as assert_error:
            RepositoryInterface()
        self.assertEqual(
            assert_error.exception.args[0],
            "Can't instantiate abstract class RepositoryInterface " +
            "with abstract methods create, delete, find_all, find_by_id, update")


@dataclass(frozen=True, kw_only=True, slots=True)
class AnyEntityStub(GenericEntity):
    foo: str
    bar: float


class InMemoryRepositoryUnitTest(unittest.TestCase):

    repo: InMemoryRepository[AnyEntityStub]

    def setUp(self) -> None:
        self.repo = InMemoryRepository()

    def test_if_entities_list_is_empty_when_created(self):
        entities = self.repo._InMemoryRepository__entities
        self.assertEqual(entities, [])

    def test_find_all_method(self):
        entity = AnyEntityStub(foo="value", bar=1.0)
        self.repo.create(entity)
        self.assertEqual(self.repo.find_all(), [entity])

    def test_create_entity_method(self):
        entity = AnyEntityStub(foo="value", bar=1.0)
        self.repo.create(entity)
        self.assertEqual(self.repo.find_all()[0], entity)

    def test_already_exists_exception_in_create_entity(self):
        self.repo.create(AnyEntityStub(foo="value", bar=1.0))
        entity = self.repo.find_all()[0]
        with self.assertRaises(Exception) as assert_error:
            self.repo.create(entity)
        self.assertEqual(
            assert_error.exception.args[0],
            f"Entity already exists using ID: {entity.id}"
        )

    def test_find_entity_by_id_method(self):
        entity = AnyEntityStub(foo="value", bar=1.0)
        self.repo.create(entity)
        found = self.repo.find_by_id(entity.id)
        self.assertEqual(found, entity)
        found = self.repo.find_by_id(entity.unique_entity_id)
        self.assertEqual(found, entity)

    def test_not_found_exception_in_find_entity_by_id(self):
        with self.assertRaises(Exception) as assert_error:
            self.repo.find_by_id("foobar")
        self.assertEqual(
            assert_error.exception.args[0],
            "Entity not found using ID: foobar"
        )
