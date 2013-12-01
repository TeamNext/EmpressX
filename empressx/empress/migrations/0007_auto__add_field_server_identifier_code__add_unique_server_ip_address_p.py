# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Server.identifier_code'
        db.add_column(u'empress_server', 'identifier_code',
                      self.gf('django.db.models.fields.CharField')(default='b48097bb-17c0-4a16-b4d2-19d0bf51e6a9', max_length=255),
                      keep_default=False)

        # Adding unique constraint on 'Server', fields ['ip_address', 'port', 'category', 'identifier_code']
        db.create_unique(u'empress_server', ['ip_address', 'port', 'category', 'identifier_code'])


    def backwards(self, orm):
        # Removing unique constraint on 'Server', fields ['ip_address', 'port', 'category', 'identifier_code']
        db.delete_unique(u'empress_server', ['ip_address', 'port', 'category', 'identifier_code'])

        # Deleting field 'Server.identifier_code'
        db.delete_column(u'empress_server', 'identifier_code')


    models = {
        u'empress.application': {
            'Meta': {'object_name': 'Application'},
            'alias': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'celery_stop_wait_secs': ('django.db.models.fields.PositiveIntegerField', [], {'default': '60'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'max_celery_worker_num': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '4'}),
            'max_worker_num': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '4'}),
            'min_celery_worker_num': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'min_worker_num': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'project_path': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'requirements': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'use_celery': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_celery_beat': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vcs': ('django.db.models.fields.CharField', [], {'default': "'Subversion'", 'max_length': '255'}),
            'vcs_password': ('django.db.models.fields.CharField', [], {'default': "'71A1Wt05Yj'", 'max_length': '255', 'blank': 'True'}),
            'vcs_path': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'vcs_username': ('django.db.models.fields.CharField', [], {'default': "'svn_t'", 'max_length': '255', 'blank': 'True'}),
            'virtualenv': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['empress.VirtualEnv']", 'null': 'True', 'blank': 'True'}),
            'wsgi_handler': ('django.db.models.fields.CharField', [], {'default': "'django.core.handlers.wsgi:WSGIHandler()'", 'max_length': '255'})
        },
        u'empress.empressmission': {
            'Meta': {'object_name': 'EmpressMission'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'date_archived': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'ex_data': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.CharField', [], {'default': "'4615b7ef-4150-4b7c-99a6-824e54c82b3d'", 'max_length': '255', 'primary_key': 'True'}),
            'retinue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['empress.Server']"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'PENDING'", 'max_length': '255'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['empress.Task']"})
        },
        u'empress.environmentvariable': {
            'Meta': {'unique_together': "(('application', 'name'),)", 'object_name': 'EnvironmentVariable'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['empress.Application']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        u'empress.hostingship': {
            'Meta': {'object_name': 'HostingShip'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['empress.Application']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_deprecated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['empress.Server']"})
        },
        u'empress.server': {
            'Meta': {'unique_together': "(('ip_address', 'port', 'category'), ('ip_address', 'port', 'category', 'identifier_code'))", 'object_name': 'Server'},
            'affinity': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'applications': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['empress.Application']", 'through': u"orm['empress.HostingShip']", 'symmetrical': 'False'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier_code': ('django.db.models.fields.CharField', [], {'default': "'67492a1c-ef34-4925-9f5c-683bef9bbc82'", 'max_length': '255'}),
            'ip_address': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_heartbeat': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {'default': '80'})
        },
        u'empress.task': {
            'Meta': {'object_name': 'Task'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'app_name': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'date_archived': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'ex_data': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.CharField', [], {'default': "'c44902ed-e61a-45ed-9c72-9619d100993a'", 'max_length': '255', 'primary_key': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'PENDING'", 'max_length': '255'})
        },
        u'empress.virtualenv': {
            'Meta': {'object_name': 'VirtualEnv'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['empress']