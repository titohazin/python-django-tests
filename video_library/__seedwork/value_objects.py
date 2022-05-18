from dataclasses import dataclass, field
from __seedwork.exceptions import InvalidUuidException
import uuid


@dataclass()
class UniqueEntityId:

    id_: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self):
        self.id_ = str(self.id_) if isinstance(self.id_, uuid.UUID) else self.id_
        self.__validate()

    def __validate(self):
        try:
            uuid.UUID(self.id_)
        except ValueError as ex:
            raise InvalidUuidException() from ex
