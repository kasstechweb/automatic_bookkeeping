

import os
from uuid import uuid4


def path_and_rename(instance, filename):
    upload_to = "statements"
    # print(instance)
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