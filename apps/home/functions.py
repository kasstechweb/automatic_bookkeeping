from django.conf import settings

def handle_uploaded_file(f):
    print('handling ' + settings.MEDIA_ROOT + f.name)
    destination = open(settings.MEDIA_ROOT + f.name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()