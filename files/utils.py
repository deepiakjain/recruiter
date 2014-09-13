import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
#from django_extensions.utils import uuid
import uuid


def get_temporary_text_file():
    io = StringIO.StringIO()
    io.write('fake\n')
    text_file = InMemoryUploadedFile(io, None, 'fake.txt', 'text', io.len, None)
    text_file.seek(0)
    return text_file


def make_uuid():
    return str(uuid.uuid4())

