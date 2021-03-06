from typing import Dict
from rest_framework import serializers

from core.domain.__seedwork.validators import (
    DRFFieldsValidator, DRFStrictBooleanField, DRFStrictCharField
)


class CategoryRules(serializers.Serializer):
    name = DRFStrictCharField(min_length=3, max_length=255)
    description = DRFStrictCharField(
        required=False, allow_null=True, allow_blank=True, max_length=255)
    is_active = DRFStrictBooleanField(required=False)
    created_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False, allow_null=True)


class CategoryValidator(DRFFieldsValidator):
    def validate(self, data: Dict) -> bool:
        rules = CategoryRules(data=data if data is not None else {})
        return super().validate(rules)
