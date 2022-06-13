from abc import ABC

from domain.__seedwork.repositories import (
    RepositoryInterface,
    SearchParams as DefaultSearchParams,
    SearchResult as DefaultSearchResult,
)

from domain.category.entities import Category


class _SearchParams(DefaultSearchParams):
    pass


class _SearchResult(DefaultSearchResult):
    pass


class CategoryRepository(
    RepositoryInterface[
        Category,
        _SearchParams,
        _SearchResult
    ],
    ABC
):
    SearchParams = _SearchParams
    SearchResult = _SearchResult
