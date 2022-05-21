from abc import ABC
import abc
from dataclasses import dataclass
from typing import Any, Dict, Generic, List, TypeVar

from .exceptions import ValidationException


@dataclass(frozen=True, slots=True)
class Validator:

    value: Any
    prop: str

    @staticmethod
    def rules(value: Any, prop: str):
        return Validator(value, prop)

    def required(self) -> 'Validator':
        if self.value is None or self.value == '':
            raise ValidationException(f'{self.prop} is required')
        return self

    def string(self) -> 'Validator':
        if self.value is not None and not isinstance(self.value, str):
            raise ValidationException(f'{self.prop} must be a string')
        return self

    def min_length(self, min: int) -> 'Validator':
        if self.value is not None and len(self.value) < min:
            raise ValidationException(
                f'{self.prop} must be equal or greater than {min} characters')
        return self

    def max_length(self, max: int) -> 'Validator':
        if self.value is not None and len(self.value) > max:
            raise ValidationException(
                f'{self.prop} must be equal or less than {max} characters')
        return self

    def boolean(self) -> 'Validator':
        if self.value is not None and self.value is not True and self.value is not False:
            raise ValidationException(f'{self.prop} must be a boolean')
        return self


FieldsErrs = Dict[str, List[str]]
T = TypeVar('T')


@dataclass(slots=True)
class ValidatorFieldsInterface(ABC, Generic[T]):

    fields_errs: FieldsErrs = None
    validated_data: T = None

    @abc.abstractmethod
    def _validate(self, data: Any) -> bool: ...
