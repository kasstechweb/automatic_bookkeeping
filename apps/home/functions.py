import os
from uuid import uuid4
from django.conf import settings

def handle_uploaded_file(f):
    print('handling ' + settings.MEDIA_ROOT + f.name)
    destination = open(settings.MEDIA_ROOT + f.name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

# def update_filename(instance, filename):
#     path = "documents/%Y/%m/%d"
#     format = instance.userid + instance.transaction_uuid + instance.file_extension
#     return os.path.join(path, format)

def unique_filename(path):
    """
    Enforce unique upload file names.
    Usage:
    class MyModel(models.Model):
        file = ImageField(upload_to=unique_filename("path/to/upload/dir"))
    """
    import os, base64, datetime
    def _func(instance, filename):
        name, ext = os.path.splitext(filename)
        name = bytes(name.encode('utf-8'))
        datetimenow = bytes(str(datetime.datetime.now()).encode('utf-8'))
        name = bytes(base64.urlsafe_b64encode(name + datetimenow)).encode('utf-8')
        return os.path.join(path, name + ext).encode('utf-8')
    return _func


def path_and_rename(instance, filename):
    upload_to = "statements"
    # ext = filename.split('.')[-1]
    # if filename.split('.')[-1] != 'pdf':
        # print('error pdf')
        # msg = 'error pdf'
    ext = 'pdf'
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)
