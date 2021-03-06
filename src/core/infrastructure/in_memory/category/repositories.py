from typing import List

from core.domain.__seedwork.repositories import InMemoryRepository
from core.domain.category.repositories import CategoryRepository
from core.domain.category.entities import Category


class CategoryInMemoryRepository(CategoryRepository, InMemoryRepository):

    sortable_fields: List[str] = [
        'name',
        'description',
        'created_at',
        'updated_at',
        'is_active'
    ]

    def _apply_filter(self, items: List[Category], filter_: str | None) -> List[Category]:
        if filter_:
            filtered = filter(lambda item: filter_.lower() in item.name.lower(), items)
            return list(filtered)
        return items

    def _apply_sort(
        self, items: List[Category],
        sort_by: str | None = None, sort_dir: str | None = None
    ) -> List[Category]:
        sort_by = 'created_at' if sort_by is None or\
            sort_by not in self.sortable_fields else sort_by
        return super()._apply_sort(items, sort_by, sort_dir)
