import re
from django.core.exceptions import ValidationError

class CustomValidator:
    
    def validate(self, password, user=None):
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                "This password must contain at least one uppercase letter."
            )
        if not re.search(r'[0-9]', password):
            raise ValidationError(
                "This password must contain at least one number."
            )
        if not re.search(r'[^a-zA-Z0-9]', password):
            raise ValidationError(
                "This password must contain at least one special character."
            )

    def get_help_text(self):
        return (
            "Your password must contain at least one uppercase letter, "
            "one number, and one special character (ex @, #, $, %, etc)."
        )