from dataclasses import dataclass
from typing import Optional

from core.domain.__seedwork.exceptions import EntityValidationException
from core.domain.__seedwork.entities import GenericEntity

from .validators import CategoryValidator


@dataclass(kw_only=True, frozen=True, slots=True)
class Category(GenericEntity):

    name: str
    description: Optional[str] = None

    def __post_init__(self):
        super(Category, self).__post_init__()
        self.__validate()

    def update(self, name: str, description: str = None):
        if description is None:
            self._set_attr('name', name)
        else:
            self._set_attrs_dict({'name': name, 'description': description})
        self.__validate()

    def __validate(self):
        validator = CategoryValidator()
        if not validator.validate(self.to_dict()):
            raise EntityValidationException(validator.fields_errors)
