from abc import ABC

from .entities import Category
from __seedwork.repositories import (
    SearchableRepositoryInterface,
    SearchParams as DefaultSearchParams,
    SearchResult as DefaultSearchResult,
)


class _SearchParams(DefaultSearchParams):
    pass


class _SearchResult(DefaultSearchResult):
    pass


class CategoryRepository(SearchableRepositoryInterface[Category, _SearchParams, _SearchResult], ABC):

    SearchParams = _SearchParams
    SearchResult = _SearchResult
