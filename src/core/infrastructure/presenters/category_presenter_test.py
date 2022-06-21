import datetime
import json
import unittest
import uuid

from core.usecase.category.use_cases import (
    CreateCategoryUseCase,
    GetCategoryUseCase,
    ListCategoryUseCase,
    UpdateCategoryUseCase
)

from .category_presenter import CategoryPresenter


class CategoryPresenterUnitTest(unittest.TestCase):

    def test_create_category_use_case_output_to_json(self):
        data_test = {
            'id': str(uuid.uuid4()),
            'name': 'foo',
            'description': 'bar',
            'is_active': True,
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
        }
        json_output = CategoryPresenter.output_to_json(
            CreateCategoryUseCase.Output(**data_test)
        )
        self.assertEqual(
            json.dumps(data_test, indent=4, default=str),
            json_output
        )

    def test_get_category_use_case_output_to_json(self):
        data_test = {
            'id': str(uuid.uuid4()),
            'name': 'foo',
            'description': 'bar',
            'is_active': True,
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
        }
        json_output = CategoryPresenter.output_to_json(
            GetCategoryUseCase.Output(**data_test)
        )
        self.assertEqual(
            json.dumps(data_test, indent=4, default=str),
            json_output
        )

    def test_update_category_use_case_output_to_json(self):
        data_test = {
            'id': str(uuid.uuid4()),
            'name': 'foo',
            'description': 'bar',
            'is_active': True,
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
        }
        json_output = CategoryPresenter.output_to_json(
            UpdateCategoryUseCase.Output(**data_test)
        )
        self.assertEqual(
            json.dumps(data_test, indent=4, default=str),
            json_output
        )

    def test_list_category_use_case_output_to_json(self):
        data_test = {
            'items': [
                {
                    'id': str(uuid.uuid4()),
                    'name': 'foo',
                    'description': 'bar',
                    'is_active': True,
                    'created_at': datetime.datetime.now(),
                    'updated_at': datetime.datetime.now(),
                },
                {
                    'id': str(uuid.uuid4()),
                    'name': 'bar',
                    'description': 'foo',
                    'is_active': False,
                    'created_at': datetime.datetime.now(),
                    'updated_at': datetime.datetime.now(),
                }
            ],
            'total': 2,
            'current_page': 1,
            'per_page': 2,
            'last_page': 1
        }
        json_output = CategoryPresenter.output_to_json(
            ListCategoryUseCase.Output(**data_test)
        )
        self.assertEqual(
            json.dumps(data_test, indent=4, default=str),
            json_output
        )
        print(json_output)
