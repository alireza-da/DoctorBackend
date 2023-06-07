import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage

class MyFileStorage(FileSystemStorage):

    # This method is actually defined in Storage
    def get_available_name(self, name):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

def content_file_name(instance, filename):
    return '/'.join(['content/users', instance.email, filename])

def message_file_name(instance, filename):
    return '/'.join(['messages/users', instance.type, filename])

def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)