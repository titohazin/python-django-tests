from abc import ABC
import abc
import copy
from dataclasses import dataclass, field
import math
from typing import Any, List, Optional, TypeVar, Generic

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


Input = TypeVar('Input')
Output = TypeVar('Output')


class SearchableRepositoryInterface(Generic[T, Input, Output], RepositoryInterface[T], ABC):

    @abc.abstractmethod
    def search(self, input_: Input) -> List[Output]: ...


# sourcery skip: avoid-builtin-shadow
Filter = TypeVar('Filter', str, Any)


@dataclass(slots=True, kw_only=True)
class SearchParams(Generic[Filter]):

    page: Optional[int] = 1
    per_page: Optional[int] = 10
    sort_by: Optional[str] = None
    sort_dir: Optional[str] = None
    filter: Optional[Filter] = None

    def __post_init__(self):
        self.__normalize_page()
        self.__normalize_per_page()
        self.__normalize_sort_by()
        self.__normalize_sort_dir()
        self.__normalize_filter()

    def __normalize_page(self):
        default = self.__get_dataclass_field('page').default
        page = self.__convert_value_to_int(self.page, default)
        self.page = default if page < 1 else page

    def __normalize_per_page(self):
        default = self.__get_dataclass_field('per_page').default
        per_page = self.__convert_value_to_int(self.per_page, default)
        self.per_page = default if per_page < 1 else per_page

    def __normalize_sort_by(self):
        self.sort_by = None if self.sort_by == '' or self.sort_by is None \
            else str(self.sort_by)

    def __normalize_sort_dir(self):
        if self.sort_dir == '' or self.sort_dir is None:
            self.sort_dir = None
            return
        sort_dir = str(self.sort_dir).lower()
        self.sort_dir = 'asc' if sort_dir not in ['asc', 'desc'] else sort_dir

    def __normalize_filter(self):
        self.filter = None if self.filter == '' or self.filter is None \
            else str(self.filter)

    def __convert_value_to_int(self, value: Any, default=0) -> int:
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    def __get_dataclass_field(self, field_name: str) -> Any:
        return SearchParams.__dataclass_fields__[field_name]


@dataclass(slots=True, kw_only=True, frozen=True)
class SearchResult(Generic[T, Filter]):

    items: List[T]
    total: int
    current_page: int
    per_page: int
    last_page: int = field(init=False)
    sort_by: Optional[str] = None
    sort_dir: Optional[str] = None
    filter: Optional[Filter] = None

    def __post_init__(self):
        object.__setattr__(self, 'last_page', math.ceil(
            self.total / self.per_page))

    def to_dict(self) -> dict:
        return {
            'items': self.items,
            'total': self.total,
            'current_page': self.current_page,
            'per_page': self.per_page,
            'last_page': self.last_page,
            'sort_by': self.sort_by,
            'sort_dir': self.sort_dir,
            'filter': self.filter
        }


@dataclass(slots=True)
class InMemoryRepository(Generic[T], RepositoryInterface[T]):

    __entities: List[T] = field(default_factory=lambda: [])

    def find_all(self) -> List[T]:
        return copy.copy(self.__entities)

    def find_by_id(self, id_: str | UniqueEntityId) -> T:
        entity = next(filter(lambda e: e.id == str(id_), self.__entities), None)
        if entity is None:
            raise EntityNotFoundException(
                f'Entity not found using ID: {id_}')
        else:
            return copy.copy(entity)

    def create(self, entity: T) -> None:
        found = next(filter(lambda e: e.id == str(entity.id), self.__entities), None)
        if found is None:
            self.__entities.append(copy.copy(entity))
        else:
            raise EntityAlreadyExistsException(
                f'Entity already exists using ID: {entity.id}')

    def update(self, entity: T) -> None:
        found = self.find_by_id(entity.id)
        found_index = self.__entities.index(found)
        self.__entities[found_index] = copy.copy(entity)

    def delete(self, id_: str | UniqueEntityId) -> None:
        self.__entities.remove(self.find_by_id(id_))
