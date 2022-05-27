from dataclasses import dataclass
import unittest

from .entities import GenericEntity
from .repositories import InMemoryRepository, RepositoryInterface, SearchableRepositoryInterface


class RepositoryInterfaceUnitTest(unittest.TestCase):

    def test_if_are_a_abstract_class_and_abstract_methods(self):
        with self.assertRaises(TypeError) as assert_error:
            RepositoryInterface()
        self.assertEqual(
            assert_error.exception.args[0],
            "Can't instantiate abstract class RepositoryInterface " +
            "with abstract methods create, delete, find_all, find_by_id, update")


class SearchableRepositoryInterfaceUnitTest(unittest.TestCase):

    def test_if_are_a_abstract_class_and_abstract_methods(self):
        with self.assertRaises(TypeError) as assert_error:
            SearchableRepositoryInterface()
        self.assertEqual(
            assert_error.exception.args[0],
            "Can't instantiate abstract class SearchableRepositoryInterface with " +
            "abstract methods create, delete, find_all, find_by_id, search, update")


@dataclass(frozen=True, kw_only=True, slots=True)
class EntityStub(GenericEntity):
    foo: str = "value"
    bar: float = 1.0

    def update(self, foo: str) -> None:
        self._set_attr('foo', foo)


class InMemoryRepositoryUnitTest(unittest.TestCase):

    repo: InMemoryRepository[EntityStub]

    def setUp(self) -> None:
        self.repo = InMemoryRepository()

    def test_if_entities_list_is_empty_when_created(self):
        entities = self.repo._InMemoryRepository__entities
        self.assertEqual(entities, [])

    def test_find_all_method(self):
        entity = EntityStub()
        self.repo.create(entity)
        # Test without change source entity state
        self.assertEqual(self.repo.find_all(), [entity])
        # Change source entity state without updating repository
        entity.update(foo="other value")  # NOSONAR
        self.assertNotEqual(self.repo.find_all(), [entity])

    def test_create_entity_method(self):
        entity = EntityStub()
        self.repo.create(entity)
        self.assertEqual(self.repo.find_all()[0], entity)

    def test_already_exists_exception_in_create_entity(self):
        self.repo.create(EntityStub())
        entity = self.repo.find_all()[0]
        with self.assertRaises(Exception) as assert_error:
            self.repo.create(entity)
        self.assertEqual(
            assert_error.exception.args[0],
            f"Entity already exists using ID: {entity.id}"
        )

    def test_find_by_id_method(self):
        entity = EntityStub()
        self.repo.create(entity)
        # Test without change source entity state
        found = self.repo.find_by_id(entity.unique_entity_id)
        self.assertEqual(found, entity)
        found = self.repo.find_by_id(entity.id)
        self.assertEqual(found, entity)
        # Change source entity state without updating repository
        found = self.repo.find_by_id(entity.id)
        entity.update(foo="other value")
        self.assertNotEqual(found, entity)

    def test_not_found_exception_in_find_entity_by_id(self):
        with self.assertRaises(Exception) as assert_error:
            self.repo.find_by_id("fake id")
        self.assertEqual(
            assert_error.exception.args[0],
            "Entity not found using ID: fake id"
        )

    def test_update_method(self):
        entity = EntityStub()
        self.repo.create(entity)
        # Test without change source entity state
        found = self.repo.find_by_id(entity.id)
        self.assertEqual(entity, found)
        # Change source entity state without updating repository
        entity.update(foo="any value")
        found = self.repo.find_by_id(entity.id)
        self.assertNotEqual(entity, found)
        # Change source entity state and updates repository
        entity.update(foo="other value")
        self.repo.update(entity)
        found = self.repo.find_by_id(entity.id)
        self.assertEqual(entity, found)

    def test_not_found_exception_in_update_entity(self):
        entity = EntityStub()
        with self.assertRaises(Exception) as assert_error:
            self.repo.update(entity)
        self.assertEqual(
            assert_error.exception.args[0],
            f"Entity not found using ID: {entity.id}"
        )

    def test_delete_method(self):
        entity = EntityStub()
        self.repo.create(entity)
        found = self.repo.find_by_id(entity.id)
        self.assertEqual(entity, found)
        self.repo.delete(entity.id)
        with self.assertRaises(Exception) as assert_error:
            self.repo.find_by_id(entity.id)
        self.assertEqual(
            assert_error.exception.args[0],
            f"Entity not found using ID: {entity.id}"
        )
        self.repo.create(entity)
        self.repo.delete(entity.unique_entity_id)
        with self.assertRaises(Exception) as assert_error:
            self.repo.find_by_id(entity.unique_entity_id)
        self.assertEqual(
            assert_error.exception.args[0],
            f"Entity not found using ID: {entity.unique_entity_id}"
        )

    def test_not_found_exception_in_delete_entity(self):
        with self.assertRaises(Exception) as assert_error:
            self.repo.delete('fake id')
        self.assertEqual(
            assert_error.exception.args[0],
            "Entity not found using ID: fake id"
        )
