from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar

from core.domain.__seedwork.repositories import Filter, SearchResult


@dataclass(slots=True, frozen=True)
class SearchInput(Generic[Filter]):
    page: Optional[int] = None
    per_page: Optional[int] = None
    sort_by: Optional[str] = None
    sort_dir: Optional[str] = None
    filter_: Optional[Filter] = None


Item = TypeVar('Item')


@dataclass(slots=True, frozen=True)
class SearchOutput(Generic[Item]):
    items: List[Item]
    total: int
    current_page: int
    per_page: int
    last_page: int


Output = TypeVar('Output', bound=SearchOutput)


@dataclass(slots=True, frozen=True)
class SearchOutputMapper:

    __child: Output

    @staticmethod
    def from_child(child: Output) -> 'SearchOutputMapper':
        return SearchOutputMapper(child)

    def to_output(self, items: List[Item], result: SearchResult) -> SearchOutput[Item]:
        return self.__child(
            items=items,
            total=result.total,
            current_page=result.current_page,
            per_page=result.per_page,
            last_page=result.last_page
        )
