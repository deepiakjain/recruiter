import logging
import posixpath
from django.shortcuts import get_object_or_404
from files.models import UUIDFile
from django.contrib.auth.decorators import login_required
from recruiter import settings
from django.views.static import serve
from django.http.response import HttpResponse


def download_file(request, file_path, file_name, protected=False):

    if file_name == '':
        # from download_uuid_file
        file_name = posixpath.split(file_path)[1]
    else:
        # from url
        file_path = posixpath.join(file_path, file_name)

    if protected:
        root = settings.PROTECTED_FILES_ROOT
        url = settings.PROTECTED_FILES_URL
    else:
        root = settings.MEDIA_ROOT
        url = settings.MEDIA_URL

    if not settings.ENABLE_ACCEL_REDIRECT:
            response = serve(request, file_path, root)
            response['Content-Disposition'] = "attachment; filename=" + file_name.encode('utf-8')
    else:
        file_url = url + file_path
        response = HttpResponse('')
        response['X-Accel-Redirect'] = file_url.encode('utf-8')
        response['Content-Type'] = ''
        response['Content-Disposition'] = "attachment; filename=" + file_name.encode('utf-8')

    return response


@login_required
def download_uuid_file(request, file_uuid):

    uuid_file = get_object_or_404(UUIDFile, file_uuid=file_uuid)
    return download_file(request, uuid_file.file_path, '', True)
