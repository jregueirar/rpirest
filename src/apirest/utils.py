# Code from https://docs.djangoproject.com/es/1.10/topics/http/file-uploads/
def save_uploaded_file_to_disk(path, f):
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    destination.close()
    return path