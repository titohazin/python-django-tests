from abc import ABC

from .entities import Category
from __seedwork.repositories import RepositoryInterface


class CategoryRepository(RepositoryInterface[Category], ABC):
    pass
