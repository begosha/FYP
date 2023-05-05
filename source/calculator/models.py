from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from safedelete.models import SafeDeleteModel, SOFT_DELETE

from .mixins import FileUploadToMixin


User = get_user_model()


class TimeStampAbstract(models.Model):
    created_at = models.DateTimeField(
        verbose_name=_('Created at'),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_('Updated at'),
        auto_now=True,
    )

    class Meta:
        abstract = True
        get_latest_by = '-pk'

    def touch(self, commit: bool = False) -> None:
        """Updates "updated_at" field."""
        self.updated_at = timezone.now()
        if commit:
            self.save(update_fields=('updated_at',))

    def save(self, **kwargs):
        should_update = kwargs.pop('should_update', True)

        if kwargs.get('update_fields') and should_update:
            kwargs['update_fields'] = {
                *kwargs.get('update_fields'),
                'updated_at',
            }

        return super().save(**kwargs)


class Transaction(TimeStampAbstract, SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE

    positions = models.JSONField(
        encoder=None,
        null=True,
    )
    total_check = models.IntegerField(
        verbose_name='Total Check',
        null=True,
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='transactions',
        related_query_name='transaction',
        blank=True,
        null=True,
    )
    is_paid = models.BooleanField(
        verbose_name=_('is paid'),
        default=False,
    )


class File(TimeStampAbstract, SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE
    """File."""

    id = models.BigAutoField(
        primary_key=True,
    )
    name = models.CharField(
        verbose_name=_('Original file name'),
        null=True,
        blank=True,
        editable=False,
        max_length=255,
    )
    file = models.FileField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('File'),
    )
    description = models.TextField(
        verbose_name=_('Description'),
        blank=True,
        default='',
    )
    size = models.PositiveIntegerField(
        verbose_name=_('Size'),
        blank=True,
        null=True,
        editable=False,
    )
    meta = models.JSONField(
        verbose_name=_('Meta'),
        null=True,
        blank=True,
    )

    class Meta:
        db_table = 'file'


class FileField(models.ForeignKey):
    """File field."""

    def __init__(
        self,
        to='File',
        verbose_name=_('File'),
        on_delete=models.PROTECT,
        related_name='+',
        related_query_name=None,
        limit_choices_to=None,
        parent_link=False,
        to_field=None,
        db_constraint=True,
        **kwargs,
    ):
        super().__init__(
            verbose_name=verbose_name,
            to=to,
            on_delete=on_delete,
            related_name=related_name,
            related_query_name=related_query_name,
            limit_choices_to=limit_choices_to,
            parent_link=parent_link,
            to_field=to_field,
            db_constraint=db_constraint,
            **kwargs,
        )


class Scan(FileUploadToMixin, SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE

    image = FileField(
        verbose_name=_('Scan'),
        blank=True,
        null=True,
        help_text=_('Image taken or uploaded'),
        related_name='scan',
    )

    position = models.ForeignKey(
        verbose_name=_('Position'),
        to='Position',
        related_name='scans',
        related_query_name='scan',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        db_table = 'scan'
        verbose_name = _('Scan')
        verbose_name_plural = _('Scans')


class Position(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE

    name = models.CharField(
        verbose_name=_('Position name'),
        max_length=255,
        blank=True,
        null=True,
    )
    price = models.IntegerField(
        verbose_name=_('Position Price'),
        blank=True,
        null=True,
    )
    image = FileField(
        verbose_name=_('Position'),
        blank=True,
        null=True,
        help_text=_('Image of the position'),
        related_name='position',
    )

    class Meta:
        db_table = 'position'
        verbose_name = _('Position')
        verbose_name_plural = _('Positions')


class ModelFile(TimeStampAbstract, SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE
    name = models.CharField(
        verbose_name=_('Position name'),
        max_length=255,
        blank=True,
        null=True,
    )
    model = FileField(
        verbose_name=_('ModelFile'),
        blank=True,
        null=True,
        help_text=_('Trained model'),
        related_name='modelfile',
    )

    class Meta:
        db_table = 'modelfile'
        verbose_name = _('Model File')
        verbose_name_plural = _('Model Files')
