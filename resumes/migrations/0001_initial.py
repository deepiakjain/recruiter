# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Qualification'
        db.create_table(u'resumes_qualification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=70)),
        ))
        db.send_create_signal(u'resumes', ['Qualification'])

        # Adding model 'JobDetails'
        db.create_table(u'resumes_jobdetails', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('father_name', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('qualification', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['resumes.Qualification'])),
            ('resume', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('apply_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('job_code', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('experience', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'resumes', ['JobDetails'])


    def backwards(self, orm):
        # Deleting model 'Qualification'
        db.delete_table(u'resumes_qualification')

        # Deleting model 'JobDetails'
        db.delete_table(u'resumes_jobdetails')


    models = {
        u'resumes.jobdetails': {
            'Meta': {'object_name': 'JobDetails'},
            'apply_date': ('django.db.models.fields.DateTimeField', [], {}),
            'experience': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'father_name': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_code': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'qualification': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['resumes.Qualification']"}),
            'resume': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        u'resumes.qualification': {
            'Meta': {'object_name': 'Qualification'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '70'})
        }
    }

    complete_apps = ['resumes']