from abc import ABC
import abc
from dataclasses import dataclass
from typing import Any, Dict, Generic, List, TypeVar

from rest_framework.serializers import Serializer
from rest_framework.serializers import CharField
from rest_framework.serializers import BooleanField


FieldsErrors = Dict[str, List[str]]
T = TypeVar('T')


@dataclass(slots=True)
class FieldsValidatorInterface(ABC, Generic[T]):

    fields_errors: FieldsErrors = None
    validated_data: T = None

    @abc.abstractmethod
    def validate(self, data: Any) -> bool:
        ...


class DRFFieldsValidator(FieldsValidatorInterface[T], ABC):

    def validate(self, serializer: Serializer) -> bool:
        if serializer.is_valid():
            self.validated_data = dict(serializer.validated_data)
            return True
        else:
            self.fields_errors = {
                field: [str(error) for error in errors]
                for field, errors in serializer.errors.items()
            }
            return False


class DRFStrictCharField(CharField):

    def to_internal_value(self, data):
        if not isinstance(data, str) and data is not None:
            self.fail('invalid')
        return super().to_internal_value(data)


class DRFStrictBooleanField(BooleanField):

    def to_internal_value(self, data):
        if data is not None:
            return data if isinstance(data, bool) \
                else self.fail('invalid', input=data)
        return super().to_internal_value(data)
