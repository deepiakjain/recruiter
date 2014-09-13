import os
from django.db import models
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
import posixpath
from files.utils import make_uuid
from files.file_upload_handlers import *


class BaseFile(models.Model):

    file_path = models.CharField(max_length=400, editable=False, db_index=True)

    class Meta:
        abstract = True

    @property
    def file_name(self):
        return posixpath.split(self.file_path)[1]


class UUIDFile(BaseFile):
    file_uuid = models.CharField(max_length=36, editable=False, db_index=True, unique=True)


@receiver(post_save, sender=UUIDFile)
def generate_file_uuid(sender, **kwargs):
    if kwargs['created']:
        saved_file = kwargs['instance']
        saved_file.file_uuid = make_uuid()
        saved_file.save()


class FileServersInfo(models.Model):
    file_servers = models.FileField(upload_to=file_servers_info_upload_to,
                                    max_length=1000)

    @property
    def file_name(self):
        if self.file_servers:
            return os.path.basename(self.file_servers.file.name)
        else:
            return ''

    def __unicode__(self):
        return str(self.file_servers)

