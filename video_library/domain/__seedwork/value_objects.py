from abc import ABC
from dataclasses import dataclass, field, fields
import json
import uuid

from .exceptions import InvalidUuidException


@dataclass(frozen=True, slots=True)
class GenericValueObject(ABC):

    def __str__(self) -> str:

        class_fields = fields(self)
        fields_names = [field.name for field in class_fields]

        if len(fields_names) == 1:
            return str(getattr(self, fields_names[0]))
        else:
            return json.dumps({
                field_name: getattr(self, field_name) for field_name in fields_names
            })


@dataclass(frozen=True, slots=True)
class UniqueEntityId(GenericValueObject):

    id_: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self):
        parsed_id = str(self.id_) if isinstance(self.id_, uuid.UUID) else self.id_
        object.__setattr__(self, 'id_', parsed_id)
        self.__validate()

    def __validate(self):
        try:
            uuid.UUID(self.id_)
        except ValueError as ex:
            raise InvalidUuidException() from ex
