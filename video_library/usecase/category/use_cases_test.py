import copy
import random
import unittest
from typing import Optional
from unittest.mock import patch

from django.conf import settings

from domain.__seedwork.exceptions import EntityNotFoundException
from domain.category.entities import Category
from infrastructure.category.repositories import (
    CategoryInMemoryRepository, CategoryRepository
)

from usecase.__seedwork.use_cases import GenericUseCase
from usecase.__seedwork.dto import SearchInput, SearchOutput

from .dto import CategoryOutput, CategoryOutputMapper
from .use_cases import (
    CreateCategoryUseCase,
    GetCategoryUseCase,
    ListCategoryUseCase,
    UpdateCategoryUseCase,
    DeleteCategoryUseCase
)


class CreateCategoryUseCaseUnitTests(unittest.TestCase):

    repo: CategoryInMemoryRepository
    create_category: CreateCategoryUseCase

    def setUp(self) -> None:
        # Required configuration for integration tests (Django)
        if not settings.configured:
            settings.configure(USE_I18N=False)
        self.repo = CategoryInMemoryRepository()
        self.create_category = CreateCategoryUseCase(self.repo)

    def test_if_implements_generic_use_case(self):
        self.assertIsInstance(self.create_category, GenericUseCase)

    def test_input_inner_class(self):
        self.assertEqual(
            CreateCategoryUseCase.Input.__annotations__,
            {
                'name': str,
                'description': Optional[str],
                'is_active': Optional[bool]
            }
        )
        self.assertEqual(
            CreateCategoryUseCase.Input.__dataclass_fields__['description'].default,
            Category.get_field_default('description')
        )
        self.assertEqual(
            CreateCategoryUseCase.Input.__dataclass_fields__['is_active'].default,
            Category.get_field_default('is_active')
        )

    def test_if_output_inner_class_is_category_output_subclass(self):
        self.assertTrue(issubclass(CreateCategoryUseCase.Output, CategoryOutput))

    def test_create_category(self):
        with patch.object(self.repo, 'insert', wraps=self.repo.insert) as mock_create:
            input_ = CreateCategoryUseCase.Input(name='foobar')
            output_ = self.create_category(input_)
            self.assertEqual(
                output_,
                CategoryOutputMapper.from_child(CreateCategoryUseCase.Output).to_output(
                    Category(
                        name='foobar',
                        unique_entity_id=self.repo._items[0].id,
                        created_at=self.repo._items[0].created_at
                    )
                )
            )
        mock_create.assert_called_once()

    def test__to_output_private_method(self):
        category = Category(name='foobar')
        output_ = self.create_category._CreateCategoryUseCase__to_output(category)
        self.assertEqual(
            output_,
            CreateCategoryUseCase.Output(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active,
                created_at=category.created_at,
                updated_at=category.updated_at
            )
        )


class GetCategoryUseCaseUnitTests(unittest.TestCase):

    repo: CategoryInMemoryRepository
    get_category: GetCategoryUseCase

    def setUp(self) -> None:
        # Required configuration for integration tests (Django)
        if not settings.configured:
            settings.configure(USE_I18N=False)
        self.repo = CategoryInMemoryRepository()
        self.get_category = GetCategoryUseCase(self.repo)

    def test_if_implements_generic_use_case(self):
        self.assertIsInstance(self.get_category, GenericUseCase)

    def test_input_inner_class(self):
        self.assertEqual(
            GetCategoryUseCase.Input.__annotations__,
            {'id_': str}
        )

    def test_if_output_inner_class_is_category_output_subclass(self):
        self.assertTrue(issubclass(GetCategoryUseCase.Output, CategoryOutput))

    def test_get_category(self):
        new_category = Category(name='foobar')
        self.repo._items = [new_category]
        with patch.object(self.repo, 'find_by_id', wraps=self.repo.find_by_id) as mock_find_by_id:
            input_ = GetCategoryUseCase.Input(new_category.id)
            output_ = self.get_category(input_)
            self.assertEqual(
                output_,
                CategoryOutputMapper.from_child(GetCategoryUseCase.Output).to_output(new_category))
        mock_find_by_id.assert_called_once()

    def test_throw_exception_if_category_not_found(self):
        with self.assertRaises(EntityNotFoundException):
            input_ = GetCategoryUseCase.Input('fake_id')
            self.get_category(input_)

    def test__to_output_private_method(self):
        category = Category(name='foobar')
        output_ = self.get_category._GetCategoryUseCase__to_output(category)
        self.assertEqual(
            output_,
            GetCategoryUseCase.Output(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active,
                created_at=category.created_at,
                updated_at=category.updated_at
            )
        )


class ListCategoryUseCaseUnitTests(unittest.TestCase):

    repo: CategoryInMemoryRepository
    list_category: ListCategoryUseCase

    def setUp(self) -> None:
        # Required configuration for integration tests (Django)
        if not settings.configured:
            settings.configure(USE_I18N=False)
        self.repo = CategoryInMemoryRepository()
        self.list_category = ListCategoryUseCase(self.repo)

    def test_if_implements_generic_use_case(self):
        self.assertIsInstance(self.list_category, GenericUseCase)

    def test_if_input_inner_class_is_search_input_subclass(self):
        self.assertTrue(issubclass(ListCategoryUseCase.Input, SearchInput))

    def test_if_output_inner_class_is_search_output_subclass(self):
        self.assertTrue(issubclass(ListCategoryUseCase.Output, SearchOutput))

    def test_list_when_pass_empty_search_params(self):
        variation = random.sample(range(9), 9)
        categories_source = [Category(
            name=f"cat_{i}", description=f"desc_{i}") for i in variation]
        self.repo._items = copy.copy(categories_source)
        random.shuffle(self.repo._items)
        with patch.object(self.repo, 'search', wraps=self.repo.search) as mock_search:
            # When no search params are passed (empty input)
            input_ = ListCategoryUseCase.Input()
            output_ = self.list_category(input_)
            # Should return all categories sorted by created_at (= categories_source)
            self.assertEqual(
                output_.items,
                # As default, search() return ten categories per page (per_page=10)):
                list(map(
                    CategoryOutputMapper.from_default_child().to_output,
                    categories_source[:10]
                ))
            )
        mock_search.assert_called_once()

    def test_list_when_pass_all_search_params(self):
        categories_source = [Category(
            name=f"cat_{i}", description=f"desc_{i}") for i in range(15)]
        self.repo._items = copy.copy(categories_source)
        random.shuffle(self.repo._items)
        with patch.object(self.repo, 'search', wraps=self.repo.search) as mock_search:
            input_ = ListCategoryUseCase.Input(
                page=2, per_page=3, sort_by='name', sort_dir='desc', filter_='cat_1'
            )
            output_ = self.list_category(input_)
            self.assertEqual(
                output_,
                ListCategoryUseCase.Output(
                    items=list(map(
                        CategoryOutputMapper.from_default_child().to_output, [
                            categories_source[11],
                            categories_source[10],
                            categories_source[1]
                        ])),
                    total=6,
                    current_page=2,
                    per_page=3,
                    last_page=2
                )
            )
        mock_search.assert_called_once()

    def test__to_output_private_method(self):
        category = Category(name='foobar')
        search_result = CategoryRepository.SearchResult(
            items=[category],
            total=1,
            current_page=1,
            per_page=10,
            sort_by=None,
            sort_dir=None,
            filter_=None
        )
        output_ = self.list_category._ListCategoryUseCase__to_output(search_result)
        self.assertEqual(
            output_,
            ListCategoryUseCase.Output(
                items=[CategoryOutputMapper.from_default_child().to_output(category)],
                total=search_result.total,
                current_page=search_result.current_page,
                per_page=search_result.per_page,
                last_page=search_result.last_page
            )
        )


class UpdateCategoryUseCaseUnitTests(unittest.TestCase):

    repo: CategoryInMemoryRepository
    update_category: UpdateCategoryUseCase

    def setUp(self) -> None:
        # Required configuration for integration tests (Django)
        if not settings.configured:
            settings.configure(USE_I18N=False)
        self.repo = CategoryInMemoryRepository()
        self.update_category = UpdateCategoryUseCase(self.repo)

    def test_if_implements_generic_use_case(self):
        self.assertIsInstance(self.update_category, GenericUseCase)

    def test_input_inner_class(self):
        self.assertEqual(
            UpdateCategoryUseCase.Input.__annotations__,
            {'id_': str, 'name': str, 'description': Optional[str]}
        )

    def test_if_output_inner_class_is_category_output_subclass(self):
        self.assertTrue(issubclass(UpdateCategoryUseCase.Output, CategoryOutput))

    def test_update_category(self):  # sourcery skip: extract-method
        new_category = Category(name='foobar')
        self.repo._items = [new_category]
        with patch.object(self.repo, 'update', wraps=self.repo.update) as mock_update:
            input_ = UpdateCategoryUseCase.Input(
                id_=new_category.id,
                name='foobar_updated',
                description='foobar_updated_description'
            )
            output_ = self.update_category(input_)
        mock_update.assert_called_once()
        found_category = self.repo.find_by_id(new_category.id)
        self.assertNotEqual(found_category, new_category)
        self.assertEqual(output_, CategoryOutputMapper.from_child(
            UpdateCategoryUseCase.Output).to_output(found_category))
        self.assertEqual(found_category.name, 'foobar_updated')
        with patch.object(self.repo, 'find_by_id', wraps=self.repo.find_by_id) as mock_find_by_id:
            self.update_category(input_)
            # 2 calls because InMemoryRepository implementation for tests (purposeful)
            self.assertEqual(mock_find_by_id.call_count, 2)

    def test_throw_exception_if_category_not_found(self):
        with self.assertRaises(EntityNotFoundException):
            input_ = UpdateCategoryUseCase.Input(id_='fake_id', name='foobar')
            self.update_category(input_)

    def test__to_output_private_method(self):
        category = Category(name='foobar')
        output_ = self.update_category._UpdateCategoryUseCase__to_output(category)
        self.assertEqual(
            output_,
            UpdateCategoryUseCase.Output(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active,
                created_at=category.created_at,
                updated_at=category.updated_at
            )
        )


class DeleteCategoryUseCaseUnitTests(unittest.TestCase):

    repo: CategoryInMemoryRepository
    delete_category: DeleteCategoryUseCase

    def setUp(self) -> None:
        # Required configuration for integration tests (Django)
        if not settings.configured:
            settings.configure(USE_I18N=False)
        self.repo = CategoryInMemoryRepository()
        self.delete_category = DeleteCategoryUseCase(self.repo)

    def test_if_implements_generic_use_case(self):
        self.assertIsInstance(self.delete_category, GenericUseCase)

    def test_input_inner_class(self):
        self.assertEqual(
            DeleteCategoryUseCase.Input.__annotations__,
            {'id_': str}
        )

    def test_delete_category(self):  # sourcery skip: extract-method
        new_category = Category(name='foobar')
        self.repo._items = [new_category]
        found_category = self.repo.find_by_id(new_category.id)
        self.assertEqual(found_category, new_category)
        input_ = DeleteCategoryUseCase.Input(id_=new_category.id)
        with patch.object(self.repo, 'delete', wraps=self.repo.delete) as mock_delete:
            self.delete_category(input_)
            self.assertEqual(self.repo.find_all(), [])
            with self.assertRaises(EntityNotFoundException):
                self.repo.find_by_id(new_category.id)
            self.assertEqual(len(self.repo._items), 1)
            self.assertFalse(self.repo._items[0].is_active)
            mock_delete.assert_called_once()
        with patch.object(self.repo, 'find_by_id', wraps=self.repo.find_by_id) as mock_find_by_id:
            self.repo._items = [new_category]
            self.delete_category(input_)
            mock_find_by_id.assert_called_once()
