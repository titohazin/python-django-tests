from dataclasses import dataclass
import datetime
from typing import Optional, TypeVar

from domain.category.entities import Category


@dataclass(slots=True, frozen=True)
class CategoryOutput:
    id: str
    name: str
    description: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


Output = TypeVar('Output', bound=CategoryOutput)


@dataclass(slots=True, frozen=True)
class CategoryOutputMapper:

    __child: Optional[Output] = CategoryOutput

    @staticmethod
    def from_child(child: Output) -> 'CategoryOutputMapper':
        return CategoryOutputMapper(child)

    @staticmethod
    def from_default_child() -> 'CategoryOutputMapper':
        return CategoryOutputMapper()

    def to_output(self, category: Category) -> CategoryOutput:
        return self.__child(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
            created_at=category.created_at,
            updated_at=category.updated_at,
        )
