from abc import ABC
import abc
from typing import Generic, TypeVar

Input = TypeVar('Input')
Output = TypeVar('Output')


class GenericUseCase(Generic[Input, Output], ABC):

    @abc.abstractmethod
    def __call__(self, input_: 'Input') -> 'Output':
        ...
