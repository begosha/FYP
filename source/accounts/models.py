from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField

__all__ = (
    'Profile',
)


class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        related_name='profile',
        on_delete=models.CASCADE,
        verbose_name='User'
    )
    phone_number = PhoneNumberField(
        null=False,
        blank=False,
        verbose_name='Phone Number'
    )

    def __str__(self):
        return self.user.get_full_name() + "'s Profile"

    class Meta:
        db_table = 'profile'
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'