import datetime as dt

from django.core.exceptions import ValidationError


def validate_year(value):
    current_year = dt.datetime.now().year
    if value > current_year:
        raise ValidationError(
            "Year of title cannot be more than current year!")
