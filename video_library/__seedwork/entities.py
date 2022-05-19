from abc import ABC
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional

from __seedwork.value_objects import UniqueEntityId


@dataclass(frozen=True, slots=True)
class GenericEntity(ABC):

    unique_entity_id: UniqueEntityId = field(
        default_factory=lambda: UniqueEntityId())

    @property
    def id(self) -> str:
        return str(self.unique_entity_id)

    is_active: Optional[bool] = True
    updated_at: Optional[datetime] = field(default_factory=lambda: datetime.now())
    created_at: Optional[datetime] = field(default_factory=lambda: datetime.now())

    def _set_attr(self, attr: str, value: any):
        object.__setattr__(self, attr, value)
        object.__setattr__(self, 'updated_at', datetime.now())
        return self

    def _set_attrs_dict(self, attrs: dict):
        for attr, value in attrs.items():
            object.__setattr__(self, attr, value)
        object.__setattr__(self, 'updated_at', datetime.now())
        return self

    def to_dict(self):
        entity_as_dict = asdict(self)
        entity_as_dict.pop('unique_entity_id')
        entity_as_dict['id'] = self.id
        return entity_as_dict

    def activate(self):
        object.__setattr__(self, 'is_active', True)

    def deactivate(self):
        object.__setattr__(self, 'is_active', False)
