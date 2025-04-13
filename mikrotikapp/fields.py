from django.db import models
import re
from django.core.exceptions import ValidationError

class LastNineDigitsPhoneField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 15  # Allow longer input for validation
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if value:
            # Remove all non-digit characters
            digits = re.sub(r'\D', '', value)
            # Get last 9 digits
            value = digits[-9:] if len(digits) >= 9 else digits
        return value

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        if value:
            # Remove all non-digit characters
            digits = re.sub(r'\D', '', value)
            if len(digits) < 9:
                raise ValidationError('Phone number must have at least 9 digits') 