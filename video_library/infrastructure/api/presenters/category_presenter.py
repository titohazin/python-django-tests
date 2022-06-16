from dataclasses import asdict
import json
from typing import Generic, TypeVar

from usecase.category.use_cases import (
    CreateCategoryUseCase,
    GetCategoryUseCase,
    ListCategoryUseCase,
    UpdateCategoryUseCase
)

T = TypeVar(
    'T',
    bound=CreateCategoryUseCase |
    GetCategoryUseCase |
    ListCategoryUseCase |
    UpdateCategoryUseCase
)


class CategoryPresenter(Generic[T]):

    @staticmethod
    def output_to_json(output: T) -> str:
        return json.dumps(asdict(output), indent=4, default=str)
