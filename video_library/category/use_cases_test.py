import unittest
from unittest.mock import patch

from django.conf import settings

from .use_cases import CreateCategoryUseCase
from infra.category.repositories import CategoryInMemoryRepository, CategoryRepositoryFactory


class CreateCategoryUseCaseUnitTests(unittest.TestCase):

    repo: CategoryInMemoryRepository
    create_category: CreateCategoryUseCase

    def setUp(self) -> None:
        # Required configuration for integration tests (Django)
        if not settings.configured:
            settings.configure(USE_I18N=False)
        self.repo = CategoryRepositoryFactory.instance()
        self.create_category = CreateCategoryUseCase(self.repo)

    def test_create_category(self):
        with patch.object(self.repo, 'insert', wraps=self.repo.insert) as mock_create:
            input_ = CreateCategoryUseCase.Input(
                name='foo',
                description='bar',
                is_active=True
            )
            output = self.create_category(input_)
            self.assertEqual(output, CreateCategoryUseCase.Output(
                id_=self.repo._items[0].id,
                name='foo',
                description='bar',
                is_active=True,
                created_at=self.repo._items[0].created_at,
                updated_at=None
            ))
        mock_create.assert_called_once()
