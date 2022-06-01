from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from .entities import Category
from .repositories import CategoryRepository


@dataclass(slots=True, frozen=True)
class CreateCategoryUseCase:

    __repo: CategoryRepository

    def __init__(self, repo: CategoryRepository):
        object.__setattr__(self, '_CreateCategoryUseCase__repo', repo)

    def __call__(self, input_: 'Input') -> 'Output':

        new_category = Category(
            name=input_.name,
            description=input_.description,
            is_active=input_.is_active,
        )

        self.__repo.insert(new_category)

        return self.Output(
            id_=new_category.id,
            name=new_category.name,
            description=new_category.description,
            is_active=new_category.is_active,
            created_at=new_category.created_at,
            updated_at=new_category.updated_at
        )

    @dataclass(slots=True, frozen=True)
    class Input:
        name: str
        description: Optional[str] = None
        is_active: Optional[bool] = False

    @dataclass(slots=True, frozen=True)
    class Output:
        id_: str
        name: str
        description: str
        is_active: bool
        created_at: datetime
        updated_at: datetime
