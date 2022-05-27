from __seedwork.repositories import InMemoryRepository
from category.entities import Category


class CategoryInMemoryRepository(InMemoryRepository[Category]):
    pass
