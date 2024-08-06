from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomUserAttributeSimilarityValidator:
    def validate(self, password, user=None):
        # Implement the actual validation logic here or leave it empty if not used.
        pass

    def get_help_text(self):
        return ""

class CustomMinimumLengthValidator:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _("A(z) Jelszó legalább %(min_length)d karakter hosszú kell legyen."),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return ""

class CustomCommonPasswordValidator:
    def validate(self, password, user=None):
        # Implement the actual validation logic here or leave it empty if not used.
        pass

    def get_help_text(self):
        return ""

class CustomNumericPasswordValidator:
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                _("A(z) Jelszó teljesen numerikus."),
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return ""
