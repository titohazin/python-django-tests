from abc import ABC
from dataclasses import Field, dataclass, field, asdict
from datetime import datetime
from typing import Any, Optional

from .value_objects import UniqueEntityId


@dataclass(frozen=True, slots=True)
class GenericEntity(ABC):

    unique_entity_id: UniqueEntityId = field(
        default_factory=lambda: UniqueEntityId())

    @property
    def id(self) -> str:
        return str(self.unique_entity_id)

    is_active: Optional[bool] = True
    created_at: Optional[datetime] = field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.created_at:
            object.__setattr__(self, 'created_at', datetime.now())

    def _set_attr(self, attr: str, value: any):
        object.__setattr__(self, attr, value)
        self.__refresh_updated_at()
        return self

    def _set_attrs_dict(self, attrs: dict):
        for attr, value in attrs.items():
            object.__setattr__(self, attr, value)
        self.__refresh_updated_at()
        return self

    def to_dict(self):
        entity_as_dict = asdict(self)
        entity_as_dict.pop('unique_entity_id')
        entity_as_dict['id'] = self.id
        return entity_as_dict

    def activate(self):
        object.__setattr__(self, 'is_active', True)
        self.__refresh_updated_at()

    def deactivate(self):
        object.__setattr__(self, 'is_active', False)
        self.__refresh_updated_at()

    def __refresh_updated_at(self):
        object.__setattr__(self, 'updated_at', datetime.now())

    @classmethod
    def get_field(cls, field_name: str) -> Field:
        return cls.__dataclass_fields__[field_name]

    @classmethod
    def get_field_default(cls, field_name: str) -> Any:
        return cls.__dataclass_fields__[field_name].default
