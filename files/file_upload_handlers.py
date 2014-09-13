'''
Created on 26-08-2012

@author: Administrator
'''
import logging
from django.core.files.storage import FileSystemStorage
from recruiter import settings
# import unicodedata
import posixpath

logger = logging.getLogger(__name__)


def file_servers_info_upload_to(instance, filename):

    # if hasattr(instance, 'subscriber'):
    #    instance = instance.subscriber

    path = posixpath.join(settings.USER_FILES_PATH, instance.username, filename)
    logger.debug('upload_to path is %s' % ( path))
    return path
