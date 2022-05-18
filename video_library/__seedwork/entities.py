from abc import ABC
from dataclasses import dataclass, field, asdict

from __seedwork.value_objects import UniqueEntityId


@dataclass(frozen=True)
class GenericEntity(ABC):

    unique_entity_id: UniqueEntityId = field(
        default_factory=lambda: UniqueEntityId())

    @property
    def id(self) -> str:
        return str(self.unique_entity_id)

    def to_dict(self):
        entity_as_dict = asdict(self)
        entity_as_dict.pop('unique_entity_id')
        entity_as_dict['id'] = self.id
        return entity_as_dict
