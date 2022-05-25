from typing import Dict, List


class InvalidUuidException(Exception):
    def __init__(self, error='ID must be a valid UUID') -> None:
        super().__init__(error)


class EntityValidationException(Exception):

    fields_errors: Dict[str, List[str]]

    def __init__(self, fields_errors: Dict[str, List[str]]) -> None:
        self.fields_errors = fields_errors
        super().__init__('Entity validation Failed')
