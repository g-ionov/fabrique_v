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

