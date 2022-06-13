from dataclasses import asdict, dataclass
from typing import Optional

from domain.category.entities import Category
from domain.category.repositories import CategoryRepository

from usecase.__seedwork.use_cases import GenericUseCase
from usecase.__seedwork.dto import SearchOutput, SearchInput, SearchOutputMapper

from .dto import CategoryOutput, CategoryOutputMapper


@dataclass(slots=True, frozen=True)
class CreateCategoryUseCase(GenericUseCase):

    __repo: CategoryRepository

    def __init__(self, repo: CategoryRepository):
        object.__setattr__(self, '_CreateCategoryUseCase__repo', repo)

    def __call__(self, input_: 'Input') -> 'Output':
        new_category = Category(
            name=input_.name,
            description=input_.description,
            is_active=input_.is_active,
        )
        self.__repo.insert(new_category)
        return self.__to_output(new_category)

    def __to_output(self, category: Category) -> 'Output':
        return CategoryOutputMapper\
            .from_child(CreateCategoryUseCase.Output)\
            .to_output(category)

    @dataclass(slots=True, frozen=True)
    class Input:
        name: str
        description: Optional[str] = Category.get_field_default('description')
        is_active: Optional[bool] = Category.get_field_default('is_active')

    @dataclass(slots=True, frozen=True)
    class Output(CategoryOutput):
        pass


@dataclass(slots=True, frozen=True)
class GetCategoryUseCase(GenericUseCase):

    __repo: CategoryRepository

    def __init__(self, repo: CategoryRepository):
        object.__setattr__(self, '_GetCategoryUseCase__repo', repo)

    def __call__(self, input_: 'Input') -> 'Output':
        found_category = self.__repo.find_by_id(input_.id_)
        return self.__to_output(found_category)

    def __to_output(self, category: Category) -> 'Output':
        return CategoryOutputMapper\
            .from_child(GetCategoryUseCase.Output)\
            .to_output(category)

    @dataclass(slots=True, frozen=True)
    class Input:
        id_: str

    @dataclass(slots=True, frozen=True)
    class Output (CategoryOutput):
        pass


@dataclass(slots=True, frozen=True)
class ListCategoryUseCase(GenericUseCase):

    __repo: CategoryRepository

    def __init__(self, repo: CategoryRepository):
        object.__setattr__(self, '_ListCategoryUseCase__repo', repo)

    def __call__(self, input_: 'Input') -> 'Output':
        search_params = self.__repo.SearchParams(**asdict(input_))
        result = self.__repo.search(search_params)
        return self.__to_output(result)

    def __to_output(self, result: CategoryRepository.SearchResult) -> 'Output':
        items = list(map(
            CategoryOutputMapper.from_default_child().to_output, result.items)
        )
        return SearchOutputMapper\
            .from_child(ListCategoryUseCase.Output)\
            .to_output(items, result)

    @dataclass(slots=True, frozen=True)
    class Input(SearchInput[str]):
        pass

    @dataclass(slots=True, frozen=True)
    class Output(SearchOutput[CategoryOutput]):
        pass


@dataclass(slots=True, frozen=True)
class UpdateCategoryUseCase(GenericUseCase):

    __repo: CategoryRepository

    def __init__(self, repo: CategoryRepository):
        object.__setattr__(self, '_UpdateCategoryUseCase__repo', repo)

    def __call__(self, input_: 'Input') -> 'Output':
        category = self.__repo.find_by_id(input_.id_)
        category.update(input_.name, input_.description)
        self.__repo.update(category)
        return self.__to_output(category)

    def __to_output(self, category: Category) -> 'Output':
        return CategoryOutputMapper\
            .from_child(UpdateCategoryUseCase.Output)\
            .to_output(category)

    @dataclass(slots=True, frozen=True)
    class Input:
        id_: str
        name: str
        description: Optional[str] = Category.get_field_default('description')

    @dataclass(slots=True, frozen=True)
    class Output(CategoryOutput):
        pass


@dataclass(slots=True, frozen=True)
class DeleteCategoryUseCase(GenericUseCase):

    __repo: CategoryRepository

    def __init__(self, repo: CategoryRepository):
        object.__setattr__(self, '_DeleteCategoryUseCase__repo', repo)

    def __call__(self, input_: 'Input') -> None:
        self.__repo.delete(input_.id_)

    @dataclass(slots=True, frozen=True)
    class Input:
        id_: str
