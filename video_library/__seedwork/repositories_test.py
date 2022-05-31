from dataclasses import dataclass
import random
from typing import Optional, List
import unittest

from .entities import GenericEntity
from .repositories import T, Filter
from .repositories import RepositoryInterface, SearchableRepositoryInterface
from .repositories import SearchParams, SearchResult
from .repositories import InMemoryRepository, InMemorySearchableRepository


@dataclass(frozen=True, kw_only=True, slots=True)
class EntityStub(GenericEntity):
    foo: str = "value"
    bar: float = 1.0

    def update(self, foo: str) -> None:
        self._set_attr('foo', foo)


class RepositoryInterfaceUnitTests(unittest.TestCase):

    def test_if_are_a_abstract_class_and_abstract_methods(self):
        with self.assertRaises(TypeError) as assert_error:
            RepositoryInterface()
        self.assertEqual(
            assert_error.exception.args[0],
            "Can't instantiate abstract class RepositoryInterface " +
            "with abstract methods create, delete, find_all, find_by_id, update")


class SearchableRepositoryInterfaceUnitTests(unittest.TestCase):

    def test_if_are_a_abstract_class_and_abstract_methods(self):
        with self.assertRaises(TypeError) as assert_error:
            SearchableRepositoryInterface()
        self.assertEqual(
            assert_error.exception.args[0],
            "Can't instantiate abstract class SearchableRepositoryInterface with " +
            "abstract methods create, delete, find_all, find_by_id, search, update")

    def test_sortable_fields_props(self):
        self.assertEqual(SearchableRepositoryInterface.sortable_fields, [])


class SearchParamsUnitTests(unittest.TestCase):

    def test_props_annotations(self):
        self.assertEqual(SearchParams.__annotations__, {
            'page': Optional[int],
            'per_page': Optional[int],
            'sort_by': Optional[str],
            'sort_dir': Optional[str],
            'filter_': Optional[Filter]
        })

    def test_props_default_value(self):
        params = SearchParams()
        # sourcery skip: class-extract-method
        self.assertEqual(params.page, 1)
        self.assertEqual(params.per_page, 10)
        self.assertIsNone(params.sort_by)
        self.assertIsNone(params.sort_dir)
        self.assertIsNone(params.filter_)

    def test_props_default_value_when_pass_none_value(self):
        params = SearchParams(
            page=None, per_page=None, sort_by=None, sort_dir=None, filter_=None)
        self.assertEqual(params.page, 1)
        self.assertEqual(params.per_page, 10)
        self.assertIsNone(params.sort_by)
        self.assertIsNone(params.sort_dir)
        self.assertIsNone(params.filter_)

    def test_props_default_value_when_pass_empty_value(self):
        params = SearchParams(
            page='', per_page='', sort_by='', sort_dir='', filter_='')
        self.assertEqual(params.page, 1)
        self.assertEqual(params.per_page, 10)
        self.assertIsNone(params.sort_by)
        self.assertIsNone(params.sort_dir)
        self.assertIsNone(params.filter_)

    def test_page_prop(self):
        arrange = [
            {'value': 9999, 'expected': 9999},
            {'value': 0, 'expected': 1},
            {'value': '0', 'expected': 1},
            {'value': 1.9, 'expected': 1},
            {'value': 1.3, 'expected': 1},
            {'value': '1', 'expected': 1},
            {'value': True, 'expected': 1},
            {'value': False, 'expected': 1},
            {'value': None, 'expected': 1},
            {'value': -1, 'expected': 1},
            {'value': '1.1', 'expected': 1},
            {'value': '', 'expected': 1},
            {'value': 'fake', 'expected': 1},
            {'value': {}, 'expected': 1},
            {'value': [], 'expected': 1}
        ]
        for i in arrange:
            msg = f'Failed with data: {i}'
            self.assertEqual(SearchParams(
                page=i['value']).page, i['expected'], msg=msg)

    def test_per_page_prop(self):
        arrange = [
            {'value': 9999, 'expected': 9999},
            {'value': 1.9, 'expected': 1},
            {'value': 1.3, 'expected': 1},
            {'value': '1', 'expected': 1},
            {'value': True, 'expected': 1},
            {'value': False, 'expected': 10},
            {'value': None, 'expected': 10},
            {'value': 0, 'expected': 10},
            {'value': '0', 'expected': 10},
            {'value': -1, 'expected': 10},
            {'value': '-1', 'expected': 10},
            {'value': '1.1', 'expected': 10},
            {'value': '', 'expected': 10},
            {'value': 'fake', 'expected': 10},
            {'value': {}, 'expected': 10},
            {'value': [], 'expected': 10}
        ]
        for i in arrange:
            msg = f'Failed with data: {i}'
            self.assertEqual(SearchParams(
                per_page=i['value']).per_page, i['expected'], msg=msg)

    def test_sort_by_prop(self):
        arrange = [
            {'value': None, 'expected': None},
            {'value': '', 'expected': None},
            {'value': 'value', 'expected': 'value'},
            {'value': 0, 'expected': '0'},
            {'value': '0', 'expected': '0'},
            {'value': -1, 'expected': '-1'},
            {'value': '-1', 'expected': '-1'},
            {'value': 1.9, 'expected': '1.9'},
            {'value': True, 'expected': 'True'},
            {'value': False, 'expected': 'False'},
            {'value': {}, 'expected': '{}'},
            {'value': [], 'expected': '[]'}
        ]
        for i in arrange:
            msg = f'Failed with data: {i}'
            self.assertEqual(SearchParams(
                sort_by=i['value']).sort_by, i['expected'], msg=msg)

    def test_sort_dir_prop_when_sort_by_is_none(self):
        arrange = [None, '', 'asc', 'desc']
        for i in arrange:
            msg = f'Failed with data: {i}'
            self.assertEqual(SearchParams(sort_dir=i).sort_dir, None, msg=msg)

    def test_sort_dir_prop_when_sort_by_is_not_none(self):
        arrange = [
            {'value': None, 'expected': 'asc'},
            {'value': '', 'expected': 'asc'},
            {'value': 'asc', 'expected': 'asc'},
            {'value': 'aSc', 'expected': 'asc'},
            {'value': 'desc', 'expected': 'desc'},
            {'value': 'desC', 'expected': 'desc'},
            {'value': 'value', 'expected': 'asc'},
            {'value': 0, 'expected': 'asc'},
            {'value': '0', 'expected': 'asc'},
            {'value': -1, 'expected': 'asc'},
            {'value': '-1', 'expected': 'asc'},
            {'value': 1.9, 'expected': 'asc'},
            {'value': True, 'expected': 'asc'},
            {'value': False, 'expected': 'asc'},
            {'value': {}, 'expected': 'asc'},
            {'value': [], 'expected': 'asc'}
        ]
        for i in arrange:
            msg = f'Failed with data: {i}'
            self.assertEqual(SearchParams(
                sort_by='foo',
                sort_dir=i['value']).sort_dir, i['expected'], msg=msg)

    def test_filter_prop(self):
        arrange = [
            {'value': None, 'expected': None},
            {'value': '', 'expected': None},
            {'value': 'value', 'expected': 'value'},
            {'value': 0, 'expected': '0'},
            {'value': '0', 'expected': '0'},
            {'value': -1, 'expected': '-1'},
            {'value': '-1', 'expected': '-1'},
            {'value': 1.9, 'expected': '1.9'},
            {'value': True, 'expected': 'True'},
            {'value': False, 'expected': 'False'},
            {'value': {}, 'expected': '{}'},
            {'value': [], 'expected': '[]'}
        ]
        for i in arrange:
            msg = f'Failed with data: {i}'
            self.assertEqual(SearchParams(filter_=i['value']).filter_, i['expected'], msg=msg)


class SearchResultUnitTests(unittest.TestCase):

    def test_props_annotations(self):
        self.assertEqual(SearchResult.__annotations__, {
            'items': List[T],
            'total': int,
            'current_page': int,
            'last_page': int,
            'per_page': int,
            'sort_by': Optional[str],
            'sort_dir': Optional[str],
            'filter_': Optional[Filter]
        })

    def test_constructor(self):
        entity_1 = EntityStub()
        entity_2 = EntityStub()
        result = SearchResult(
            items=[entity_1, entity_2],
            total=100,
            current_page=1,
            per_page=2,
            sort_by='foo',
            sort_dir='desc',
            filter_='value'
        )
        self.assertDictEqual(result.to_dict(), {
            'items': [entity_1, entity_2],
            'total': 100,
            'current_page': 1,
            'per_page': 2,
            'last_page': 50,
            'sort_by': 'foo',
            'sort_dir': 'desc',
            'filter': 'value'
        })

    def test_constructor_with_default_values(self):
        entity_1 = EntityStub()
        entity_2 = EntityStub()
        result = SearchResult(
            items=[entity_1, entity_2],
            total=100,
            current_page=1,
            per_page=2
        )
        self.assertDictEqual(result.to_dict(), {
            'items': [entity_1, entity_2],
            'total': 100,
            'current_page': 1,
            'per_page': 2,
            'last_page': 50,
            'sort_by': None,
            'sort_dir': None,
            'filter': None
        })

    def test_last_page_when_per_page_is_greater_than_total(self):
        result = SearchResult(
            items=[],
            total=4,
            current_page=1,
            per_page=10
        )
        self.assertEqual(result.last_page, 1)

    def test_last_page_when_per_page_is_less_than_total(self):
        result = SearchResult(
            items=[],
            total=100,
            current_page=1,
            per_page=10
        )
        self.assertEqual(result.last_page, 10)

    def test_last_page_when_per_page_and_total_are_not_multiples(self):
        result = SearchResult(
            items=[],
            total=91,
            current_page=1,
            per_page=10
        )
        self.assertEqual(result.last_page, 10)


class InMemoryRepositoryUnitTests(unittest.TestCase):

    repo: InMemoryRepository[EntityStub]

    def setUp(self) -> None:
        self.repo = InMemoryRepository()

    def test_if_entities_list_is_empty_when_created(self):
        entities = self.repo._items
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


class InMemorySearchableRepositoryStub(InMemorySearchableRepository[EntityStub, str]):

    sortable_fields = ['foo', 'bar']

    def _apply_filter(self, items: List[EntityStub], filter_: str | None) -> List[EntityStub]:
        if filter_:
            filtered = filter(lambda item: filter_.lower() in item.foo.lower()
                              or filter_ == str(item.bar), items)
            return list(filtered)
        return items


class InMemorySearchableRepositoryUnitTests(unittest.TestCase):

    repo: InMemorySearchableRepositoryStub

    def setUp(self) -> None:
        self.repo = InMemorySearchableRepositoryStub()

    def test_apply_filter(self):
        items = [EntityStub(foo=f"foo_{i+10}", bar=float(i+10)) for i in range(50)]
        filtered_items = self.repo._apply_filter(items, None)
        self.assertEqual(filtered_items, items)
        filtered_items = self.repo._apply_filter(items, 'foo_1')
        self.assertEqual(len(filtered_items), 10)
        filtered_items = self.repo._apply_filter(items, '10.0')
        self.assertEqual(len(filtered_items), 1)

    def test_apply_sort_when_pass_empty_props(self):
        variation = random.sample(range(3), 3)
        items = [EntityStub(foo=f"{i}", bar=float(i)) for i in variation]
        sorted_items = self.repo._apply_sort(items, None)
        self.assertEqual(sorted_items, items)
        sorted_items = self.repo._apply_sort(items, None, None)
        self.assertEqual(sorted_items, items)
        sorted_items = self.repo._apply_sort(items, None, 'asc')
        self.assertEqual(sorted_items, items)

    def test_apply_sort_when_pass_invalid_props(self):
        variation = random.sample(range(20), 20)
        items = [EntityStub(foo=f"{i}", bar=float(i)) for i in variation]
        sorted_items = self.repo._apply_sort(items, 'fake_sort_by')
        self.assertEqual(sorted_items, items)
        sorted_items = self.repo._apply_sort(items, 'foo', 'fake_sort_dir')
        self.assertEqual(sorted_items[0].foo, '0')
        self.assertEqual(sorted_items[10].foo, '18')
        self.assertEqual(sorted_items[19].foo, '9')

    def test_apply_sort_when_pass_valid_props(self):
        variation = random.sample(range(20), 20)
        items = [EntityStub(foo=f"{i}", bar=float(i)) for i in variation]
        sorted_items = self.repo._apply_sort(items, 'foo')
        self.assertEqual(sorted_items[0].foo, '0')
        self.assertEqual(sorted_items[19].foo, '9')
        sorted_items = self.repo._apply_sort(items, 'foo', 'asc')
        self.assertEqual(sorted_items[0].foo, '0')
        self.assertEqual(sorted_items[19].foo, '9')
        sorted_items = self.repo._apply_sort(items, 'bar', 'desc')
        self.assertEqual(sorted_items[0].bar, 19.0)
        self.assertEqual(sorted_items[19].bar, 0.0)

    def test_apply_pagination(self):
        variation = random.sample(range(10), 10)
        items = [EntityStub(foo=f"foo_{i}", bar=float(i)) for i in variation]
        paginated_items = self.repo._apply_pagination(items, 1, 3)
        self.assertEqual(paginated_items, items[:3])
        paginated_items = self.repo._apply_pagination(items, 2, 3)
        self.assertEqual(paginated_items, items[3:6])
        paginated_items = self.repo._apply_pagination(items, 3, 3)
        self.assertEqual(paginated_items, items[6:9])
        paginated_items = self.repo._apply_pagination(items, 4, 3)
        self.assertEqual(paginated_items, [items[9]])
        paginated_items = self.repo._apply_pagination(items, 5, 3)
        self.assertEqual(paginated_items, [])

    def test_search_when_parameters_are_empty(self):
        variation = random.sample(range(25), 25)
        items = [EntityStub(foo=f"foo_{i}", bar=float(i)) for i in variation]
        self.repo._items = items
        result = self.repo.search(SearchParams())
        self.assertEqual(result, SearchResult(
            items=items[:10],
            total=25,
            current_page=1,
            per_page=10,
            sort_by=None,
            sort_dir=None,
            filter_=None
        ))
        self.assertEqual(result.last_page, 3)

    def test_search_applying_filter_and_pagination(self):
        items = self.repo._items = [
            EntityStub(foo='foo', bar=1.0),
            EntityStub(foo='bar', bar=2.0),
            EntityStub(foo='BAR', bar=2.0),
            EntityStub(foo='FoO', bar=2.0),
            EntityStub(foo='FOO', bar=3.0),
            EntityStub(foo='Foo', bar=3.0),
        ]
        self.assertEqual(
            self.repo.search(SearchParams(page=1, per_page=2, filter_='FOO')),
            SearchResult(
                items=[items[0], items[3]],
                total=4,
                current_page=1,
                per_page=2,
                sort_by=None,
                sort_dir=None,
                filter_='FOO'
            )
        )
        self.assertEqual(
            self.repo.search(SearchParams(page=2, per_page=2, filter_='FOO')),
            SearchResult(
                items=[items[4], items[5]],
                total=4,
                current_page=2,
                per_page=2,
                sort_by=None,
                sort_dir=None,
                filter_='FOO'
            )
        )
        self.assertEqual(
            self.repo.search(SearchParams(
                page=1, per_page=1, filter_='BAR')),
            SearchResult(
                items=[items[1]],
                total=2,
                current_page=1,
                per_page=1,
                sort_by=None,
                sort_dir=None,
                filter_='BAR'
            )
        )
        self.assertEqual(
            self.repo.search(SearchParams(
                page=3, per_page=1, filter_='bAr')),
            SearchResult(
                items=[],
                total=2,
                current_page=3,
                per_page=1,
                sort_by=None,
                sort_dir=None,
                filter_='bAr'
            )
        )

    def test_search_applying_sort_and_pagination(self):
        items = self.repo._items = [
            EntityStub(foo='foo', bar=5.0),
            EntityStub(foo='bar', bar=10.0),
            EntityStub(foo='FoO', bar=2.0),
            EntityStub(foo='FOO', bar=3.0),
            EntityStub(foo='BAR', bar=7.0),
            EntityStub(foo='Foo', bar=1.0),
        ]
        self.assertEqual(
            self.repo.search(SearchParams(page=2, per_page=2, sort_by='foo')),
            SearchResult(
                items=[items[0], items[2]],
                total=6,
                current_page=2,
                per_page=2,
                sort_by='foo',
                sort_dir='asc',
                filter_=None
            )
        )
        self.assertEqual(
            self.repo.search(SearchParams(
                page=1, per_page=2, sort_by='bar', sort_dir=None)),
            SearchResult(
                items=[items[5], items[2]],
                total=6,
                current_page=1,
                per_page=2,
                sort_by='bar',
                sort_dir='asc',
                filter_=None
            )
        )
        self.assertEqual(
            self.repo.search(SearchParams(
                page=1, per_page=2, sort_by='bar', sort_dir='desc')),
            SearchResult(
                items=[items[1], items[4]],
                total=6,
                current_page=1,
                per_page=2,
                sort_by='bar',
                sort_dir='desc',
                filter_=None
            )
        )

    def test_search_when_combine_all_parameters_case_1(self):
        variation = random.sample(range(25), 25)
        items = [EntityStub(foo=f"foo_{i}", bar=float(i)) for i in variation]
        self.repo._items = items
        comp_items = sorted(
            list(filter(lambda i: i.foo in ['foo_1', 'foo_10'], items)),
            key=lambda i: i.foo,
            reverse=True
        )
        self.assertEqual(
            self.repo.search(SearchParams(
                page=4, per_page=3, sort_by='foo', sort_dir='desc', filter_='_1')),
            SearchResult(
                items=comp_items,
                total=11,
                current_page=4,
                per_page=3,
                sort_by='foo',
                sort_dir='desc',
                filter_='_1'
            )
        )

    def test_search_when_combine_all_parameters_case_2(self):
        variation = random.sample(range(25), 25)
        items = [EntityStub(foo=f"foo_{i}", bar=float(i)) for i in variation]
        self.repo._items = items
        comp_items = sorted(
            list(filter(lambda i: i.foo in ['foo_11', 'foo_12', 'foo_13'], items)),
            key=lambda i: i.foo,
            reverse=True
        )
        self.assertEqual(
            self.repo.search(SearchParams(
                page=3, per_page=3, sort_by='foo', sort_dir='desc', filter_='_1')),
            SearchResult(
                items=comp_items,
                total=11,
                current_page=3,
                per_page=3,
                sort_by='foo',
                sort_dir='desc',
                filter_='_1'
            )
        )
