from .decorators import classproperty


class FileUploadToMixin:
    @classproperty
    def upload_to(cls) -> str:
        return f'{cls._meta.model_name}'