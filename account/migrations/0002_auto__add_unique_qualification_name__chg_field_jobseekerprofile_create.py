# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Qualification', fields ['name']
        db.create_unique(u'account_qualification', ['name'])


        # Changing field 'JobSeekerProfile.create_date'
        db.alter_column(u'account_jobseekerprofile', 'create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'JobSeekerProfile.resume'
        db.alter_column(u'account_jobseekerprofile', 'resume', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True))

        # Changing field 'JobSeekerProfile.mobile_no'
        db.alter_column(u'account_jobseekerprofile', 'mobile_no', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=11, null=True))

        # Changing field 'JobSeekerProfile.qualification'
        db.alter_column(u'account_jobseekerprofile', 'qualification_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.Qualification'], null=True))

        # Changing field 'JobSeekerProfile.profile_header'
        db.alter_column(u'account_jobseekerprofile', 'profile_header', self.gf('django.db.models.fields.CharField')(max_length=130, null=True))

        # Changing field 'RecruiterProfile.website'
        db.alter_column(u'account_recruiterprofile', 'website', self.gf('django.db.models.fields.CharField')(max_length=90, null=True))

        # Changing field 'RecruiterProfile.create_date'
        db.alter_column(u'account_recruiterprofile', 'create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'RecruiterProfile.company_name'
        db.alter_column(u'account_recruiterprofile', 'company_name', self.gf('django.db.models.fields.CharField')(max_length=70, null=True))

        # Changing field 'RecruiterProfile.mobile_no'
        db.alter_column(u'account_recruiterprofile', 'mobile_no', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=11, null=True))

    def backwards(self, orm):
        # Removing unique constraint on 'Qualification', fields ['name']
        db.delete_unique(u'account_qualification', ['name'])


        # Changing field 'JobSeekerProfile.create_date'
        db.alter_column(u'account_jobseekerprofile', 'create_date', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'JobSeekerProfile.resume'
        db.alter_column(u'account_jobseekerprofile', 'resume', self.gf('django.db.models.fields.files.FileField')(default='', max_length=100))

        # Changing field 'JobSeekerProfile.mobile_no'
        db.alter_column(u'account_jobseekerprofile', 'mobile_no', self.gf('django.db.models.fields.PositiveIntegerField')(default=123456789, max_length=11))

        # Changing field 'JobSeekerProfile.qualification'
        db.alter_column(u'account_jobseekerprofile', 'qualification_id', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['account.Qualification']))

        # Changing field 'JobSeekerProfile.profile_header'
        db.alter_column(u'account_jobseekerprofile', 'profile_header', self.gf('django.db.models.fields.CharField')(default='shreeyansh jain', max_length=130))

        # Changing field 'RecruiterProfile.website'
        db.alter_column(u'account_recruiterprofile', 'website', self.gf('django.db.models.fields.CharField')(default='hhtp://google.com/', max_length=90))

        # Changing field 'RecruiterProfile.create_date'
        db.alter_column(u'account_recruiterprofile', 'create_date', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'RecruiterProfile.company_name'
        db.alter_column(u'account_recruiterprofile', 'company_name', self.gf('django.db.models.fields.CharField')(default='shajin', max_length=70))

        # Changing field 'RecruiterProfile.mobile_no'
        db.alter_column(u'account_recruiterprofile', 'mobile_no', self.gf('django.db.models.fields.PositiveIntegerField')(default=1234567890, max_length=11))

    models = {
        u'account.jobseekerprofile': {
            'Meta': {'object_name': 'JobSeekerProfile'},
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobile_no': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'null': 'True'}),
            'profile_header': ('django.db.models.fields.CharField', [], {'max_length': '130', 'null': 'True'}),
            'qualification': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.Qualification']", 'null': 'True'}),
            'resume': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'account.qualification': {
            'Meta': {'object_name': 'Qualification'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '70'})
        },
        u'account.recruiterprofile': {
            'Meta': {'object_name': 'RecruiterProfile'},
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobile_no': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'null': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '90', 'null': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['account']