from dataclasses import dataclass
import datetime


@dataclass(slots=True, frozen=True)
class CategoryOutput:
    id_: str
    name: str
    description: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class CategoryOutputMapper:
    @staticmethod
    def to_output(category) -> CategoryOutput:
        return CategoryOutput(
            id_=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
            created_at=category.created_at,
            updated_at=category.updated_at,
        )
