from abc import ABC
import abc
import copy
from dataclasses import dataclass, field
import math
from typing import Any, List, Optional, TypeVar, Generic

from .exceptions import EntityAlreadyExistsException, EntityNotFoundException
from .value_objects import UniqueEntityId
from .entities import GenericEntity

T = TypeVar('T', bound=GenericEntity)
Input = TypeVar('Input')
Output = TypeVar('Output')


class RepositoryInterface(Generic[T, Input, Output], ABC):

    sortable_fields: List[str] = []

    @abc.abstractmethod
    def insert(self, entity: T) -> None:
        ...

    @abc.abstractmethod
    def update(self, entity: T) -> None:
        ...

    @abc.abstractmethod
    def delete(self, id_: str | UniqueEntityId) -> None:
        ...

    @abc.abstractmethod
    def find_by_id(self, id_: str | UniqueEntityId) -> T:
        ...

    @abc.abstractmethod
    def find_all(self) -> List[T]:
        ...

    @abc.abstractmethod
    def search(self, input_: Input) -> Output:
        ...


# sourcery skip: avoid-builtin-shadow
Filter = TypeVar('Filter', str, Any)


@dataclass(slots=True, kw_only=True)
class SearchParams(Generic[Filter]):

    page: Optional[int] = 1
    per_page: Optional[int] = 10
    sort_by: Optional[str] = None
    sort_dir: Optional[str] = None
    filter_: Optional[Filter] = None

    def __post_init__(self):
        self.__normalize_page()
        self.__normalize_per_page()
        self.__normalize_sort_by()
        self.__normalize_sort_dir()
        self.__normalize_filter()

    def __normalize_page(self):
        default = self.__get_field('page').default
        page = self.__convert_value_to_int(self.page, default)
        self.page = default if page < 1 else page

    def __normalize_per_page(self):
        default = self.__get_field('per_page').default
        per_page = self.__convert_value_to_int(self.per_page, default)
        self.per_page = default if per_page < 1 else per_page

    def __normalize_sort_by(self):
        self.sort_by = None if self.sort_by == '' or self.sort_by is None \
            else str(self.sort_by)

    def __normalize_sort_dir(self):
        if self.sort_dir == '' or self.sort_dir is None:
            self.sort_dir = 'asc' if self.sort_by else None
            return
        if self.sort_by is None:
            self.sort_dir = None
            return
        sort_dir = str(self.sort_dir).lower()
        self.sort_dir = 'asc' if sort_dir not in ['asc', 'desc'] else sort_dir

    def __normalize_filter(self):
        self.filter_ = None if self.filter_ == '' or self.filter_ is None \
            else str(self.filter_)

    def __convert_value_to_int(self, value: Any, default=0) -> int:
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    def __get_field(self, field_name: str) -> Any:
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
    filter_: Optional[Filter] = None

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
            'filter': self.filter_
        }


@dataclass(slots=True)
class InMemoryRepository(
        Generic[T, Filter],
        RepositoryInterface[
            T, SearchParams[Filter], SearchResult[T, Filter]
        ],
        ABC):

    _items: List[T] = field(default_factory=lambda: [])

    def insert(self, entity: T) -> None:
        found = next(filter(lambda e: e.id == str(entity.id), self._items), None)
        if found is None:
            self._items.append(copy.copy(entity))
        else:
            raise EntityAlreadyExistsException(
                f'Entity already exists using ID: {entity.id}')

    def update(self, entity: T) -> None:
        found = self.find_by_id(entity.id)
        found_index = self._items.index(found)
        self._items[found_index] = copy.copy(entity)

    def delete(self, id_: str | UniqueEntityId) -> None:
        found = self.find_by_id(id_)
        found_index = self._items.index(found)
        found.deactivate()
        self._items[found_index] = copy.copy(found)

    def find_by_id(self, id_: str | UniqueEntityId) -> T:
        entity = next(filter(lambda e: e.id == str(id_), self._items), None)
        if entity is None or entity.is_active is False:
            raise EntityNotFoundException(
                f'Entity not found using ID: {id_}')
        else:
            return copy.copy(entity)

    def find_all(self) -> List[T]:
        return copy.copy(list(filter(lambda e: e.is_active, self._items)))

    def search(self, input_: SearchParams[Filter]) -> SearchResult[T, Filter]:

        items_filtered = self._apply_filter(self.find_all(), input_.filter_)
        items_sorted = self._apply_sort(
            items_filtered, input_.sort_by, input_.sort_dir)
        items_paginated = self._apply_pagination(
            items_sorted, input_.page, input_.per_page)

        return SearchResult(
            items=items_paginated,
            total=len(items_filtered),
            current_page=input_.page,
            per_page=input_.per_page,
            sort_by=input_.sort_by,
            sort_dir=input_.sort_dir,
            filter_=input_.filter_
        )

    @abc.abstractmethod
    def _apply_filter(self, items: List[T], filter: Filter | None) -> List[T]:
        ...

    def _apply_sort(
        self,
        items: List[T],
        sort_by: str | None,
        sort_dir: str | None = None
    ) -> List[T]:
        if sort_by and sort_by in self.sortable_fields:
            is_reverse = sort_dir == 'desc'
            key = (lambda i: getattr(i, sort_by).lower() if isinstance(
                getattr(i, sort_by), str) else getattr(i, sort_by))
            return sorted(items, key=key, reverse=is_reverse)
        return items

    def _apply_pagination(self, items: List[T], page: int, per_page: int) -> List[T]:
        start = (page - 1) * per_page
        limit = start + per_page
        return items[slice(start, limit)]
