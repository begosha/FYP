from django.contrib.admin import register
from safedelete.admin import SafeDeleteAdmin

from . import models


@register(models.Scan)
class ScanAdmin(SafeDeleteAdmin):
    search_fields = (
        '=id',
    )
    list_display = (
        'id',
        'position',
    )
    fields = (
        'id',
        'position',
        'image',
    )
    readonly_fields = (
        'id',
    )


@register(models.Position)
class PositionAdmin(SafeDeleteAdmin):
    search_fields = (
        '=id',
    )
    list_display = (
        'id',
        'name',
        'price',
    )
    fields = (
        'id',
        'name',
        'price',
        'image',
    )
    readonly_fields = (
        'id',
    )


@register(models.Transaction)
class TransactionAdmin(SafeDeleteAdmin):
    search_fields = (
        '=id',
    )
    list_display = (
        'id',
        'user',
        'total_check',
        'created_at',
        'updated_at',
        'deleted',
    )
    fields = (
        'id',
        'user',
        'total_check',
        'created_at',
        'updated_at',
        'deleted',
        'positions',
        'is_paid',
    )
    readonly_fields = (
        'id',
        'deleted',
        'created_at',
        'updated_at',
    )


@register(models.File)
class FileAdmin(SafeDeleteAdmin):

    list_display = (
        'id',
        'file',
        'meta',
    )
    fields = (
        'id',
        'file',
        'meta',

    )
    readonly_fields = (
        'id',
    )


@register(models.ModelFile)
class ModelFileAdmin(SafeDeleteAdmin):

    list_display = (
        'id',
        'name',
    )
    fields = (
        'id',
        'name',
        'model',
        'created_at',

    )
    readonly_fields = (
        'id',
        'created_at',
    )
