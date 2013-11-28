# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Application.use_celery'
        db.add_column(u'empress_application', 'use_celery',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Application.use_celery_beat'
        db.add_column(u'empress_application', 'use_celery_beat',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Application.min_celery_worker_num'
        db.add_column(u'empress_application', 'min_celery_worker_num',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Application.max_celery_worker_num'
        db.add_column(u'empress_application', 'max_celery_worker_num',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=4),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Application.use_celery'
        db.delete_column(u'empress_application', 'use_celery')

        # Deleting field 'Application.use_celery_beat'
        db.delete_column(u'empress_application', 'use_celery_beat')

        # Deleting field 'Application.min_celery_worker_num'
        db.delete_column(u'empress_application', 'min_celery_worker_num')

        # Deleting field 'Application.max_celery_worker_num'
        db.delete_column(u'empress_application', 'max_celery_worker_num')


    models = {
        u'empress.application': {
            'Meta': {'object_name': 'Application'},
            'alias': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
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
            'id': ('django.db.models.fields.CharField', [], {'default': "'54e253c8-04b0-4805-b761-023b16ff5276'", 'max_length': '255', 'primary_key': 'True'}),
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
            'Meta': {'unique_together': "(('ip_address', 'port', 'category'),)", 'object_name': 'Server'},
            'affinity': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'applications': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['empress.Application']", 'through': u"orm['empress.HostingShip']", 'symmetrical': 'False'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'id': ('django.db.models.fields.CharField', [], {'default': "'3e8aeaf8-800e-4632-9af8-37da1f1c1775'", 'max_length': '255', 'primary_key': 'True'}),
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