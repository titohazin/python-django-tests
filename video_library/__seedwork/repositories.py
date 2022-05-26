from abc import ABC
import abc
from dataclasses import dataclass, field
from typing import List, TypeVar, Generic

from .value_objects import UniqueEntityId
from .entities import GenericEntity
from .exceptions import EntityAlreadyExistsException, EntityNotFoundException

T = TypeVar('T', bound=GenericEntity)


class RepositoryInterface(Generic[T], ABC):

    @abc.abstractmethod
    def find_all(self) -> List[T]: ...

    @abc.abstractmethod
    def find_by_id(self, id_: str | UniqueEntityId) -> T: ...

    @abc.abstractmethod
    def create(self, entity: T) -> None: ...

    @abc.abstractmethod
    def update(self, entity: T) -> None: ...

    @abc.abstractmethod
    def delete(self, id_: str | UniqueEntityId) -> None: ...


@dataclass(slots=True)
class InMemoryRepository(RepositoryInterface[T]):

    __entities: List[T] = field(default_factory=lambda: [])

    def find_all(self) -> List[T]:
        return self.__entities

    def find_by_id(self, id_: str | UniqueEntityId) -> T:
        entity = next(filter(lambda e: e.id == str(id_), self.__entities), None)
        if entity is None:
            raise EntityNotFoundException(
                f'Entity not found using ID: {id_}')
        else:
            return entity

    def create(self, entity: T) -> None:
        found = next(filter(lambda e: e.id == str(entity.id), self.__entities), None)
        if found is None:
            self.__entities.append(entity)
        else:
            raise EntityAlreadyExistsException(
                f'Entity already exists using ID: {entity.id}')

    def update(self, entity: T) -> None:
        found = self.find_by_id(entity.id)
        found_index = self.__entities.index(found)
        self.__entities[found_index] = entity

    def delete(self, id_: str | UniqueEntityId) -> None:
        self.__entities.remove(self.find_by_id(id_))
