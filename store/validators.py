from django.core.exceptions import ValidationError
import os


def validate_file_type(file):
    file_name, extension = os.path.basename(file.name).split('.')
    if extension != 'pdf':
        raise ValidationError('Type of uploaded file should be PDF.')
