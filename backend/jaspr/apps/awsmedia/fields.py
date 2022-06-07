from django.db.models import FileField


class PrimaryFileField(FileField):
    def pre_save(self, model_instance, add):
        original_name = model_instance.file_field.name
        file = super().pre_save(model_instance, add)
        model_instance.file_field_original_name = original_name
        return file
