from typing import Generic, TypeVar


class InvalidUuidException(Exception):
    def __init__(self, error='ID must be a valid UUID') -> None:
        super().__init__(error)


T = TypeVar('T')


class EntityValidationException(Exception, Generic[T]):

    fields_errors: T

    def __init__(self, fields_errors: T) -> None:
        self.fields_errors = fields_errors
        super.__init__('Entity validation Failed')
