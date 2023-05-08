import re

from rest_framework.exceptions import ValidationError


def phone_number_validation(phone_number: str)-> bool:
    """ Phone number validation
     :arg phone_number: phone number to be validated
     :return: True if phone number is valid."""
    if not phone_number:
        raise ValidationError("Phone number is required")
    if not re.match(r'^7\d{10}$', phone_number):
        raise ValidationError("Phone number is invalid")
    return True


def filter_validator(filter_params: dict)-> bool:
    """ Filter validation
     :arg filter_params: filter params to be validated
     :return: True if filter params are valid."""
    if not filter_params:
        raise ValidationError("Filter params are required")
    if not isinstance(filter_params, dict):
        raise ValidationError("Filter params must be a dict")
    for key, value in filter_params.items():
        if key not in ('operator_code', 'tag'):
            raise ValidationError(f"Filter param {key} is invalid")
        if not isinstance(value, list):
            raise ValidationError(f"Filter param {key} must be a list")
        if not all(isinstance(item, str) for item in value):
            raise ValidationError(f"Filter param {key} must contain only strings")
    return True
