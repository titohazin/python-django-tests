from dataclasses import dataclass
from typing import Optional

from __seedwork.entities import GenericEntity


@dataclass(kw_only=True, frozen=True, slots=True)
class Category(GenericEntity):

    name: str
    description: Optional[str] = None

    def update(self, name: str, description: str):
        self._set_attrs_dict({'name': name, 'description': description})
