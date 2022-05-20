from dataclasses import dataclass
from typing import Optional

from __seedwork.entities import GenericEntity
from __seedwork.validators import Validator


@dataclass(kw_only=True, frozen=True, slots=True)
class Category(GenericEntity):

    name: str
    description: Optional[str] = None

    def __new__(cls, **kwargs):
        cls.__validate(
            name=kwargs.get('name'),
            description=kwargs.get('description')
        )
        return super(Category, cls).__new__(cls)

    def update(self, name: str, description: str = None):
        self.__validate(name=name, description=description)
        if description is None:
            self._set_attr('name', name)
        else:
            self._set_attrs_dict({'name': name, 'description': description})

    @classmethod
    def __validate(cls, name: str, description: str):
        Validator.rules(name, 'name').required(
        ).string().min_length(3).max_length(255)
        Validator.rules(description, 'description').string(
        ).max_length(255)
