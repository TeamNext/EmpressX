# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'VirtualEnv'
        db.create_table(u'empress_virtualenv', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'empress', ['VirtualEnv'])

        # Adding model 'Application'
        db.create_table(u'empress_application', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('alias', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('virtualenv', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['empress.VirtualEnv'], null=True, blank=True)),
            ('vcs', self.gf('django.db.models.fields.CharField')(default='Subversion', max_length=255)),
            ('vcs_path', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('vcs_username', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('vcs_password', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('project_path', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('requirements', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('wsgi_handler', self.gf('django.db.models.fields.CharField')(default='django.core.handlers.wsgi:WSGIHandler()', max_length=255)),
        ))
        db.send_create_signal(u'empress', ['Application'])

        # Adding model 'EnvironmentVariable'
        db.create_table(u'empress_environmentvariable', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['empress.Application'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'empress', ['EnvironmentVariable'])

        # Adding unique constraint on 'EnvironmentVariable', fields ['application', 'name']
        db.create_unique(u'empress_environmentvariable', ['application_id', 'name'])

        # Adding model 'Server'
        db.create_table(u'empress_server', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip_address', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('port', self.gf('django.db.models.fields.PositiveIntegerField')(default=80)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('last_heartbeat', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal(u'empress', ['Server'])

        # Adding unique constraint on 'Server', fields ['ip_address', 'port']
        db.create_unique(u'empress_server', ['ip_address', 'port'])

        # Adding model 'HostingShip'
        db.create_table(u'empress_hostingship', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['empress.Application'])),
            ('server', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['empress.Server'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 14, 0, 0))),
            ('date_deprecated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal(u'empress', ['HostingShip'])

        # Adding model 'Task'
        db.create_table(u'empress_task', (
            ('id', self.gf('django.db.models.fields.CharField')(default='8a682a14-416b-4004-922d-d3ed2dcd4e63', max_length=255, primary_key=True)),
            ('app_name', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('state', self.gf('django.db.models.fields.CharField')(default='PENDING', max_length=255)),
            ('data', self.gf('django.db.models.fields.TextField')(default='')),
            ('ex_data', self.gf('django.db.models.fields.TextField')(default='')),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 14, 0, 0))),
            ('date_archived', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal(u'empress', ['Task'])

        # Adding model 'EmpressMission'
        db.create_table(u'empress_empressmission', (
            ('id', self.gf('django.db.models.fields.CharField')(default='3aa18fa7-0071-41a0-8bf8-15aea78fd467', max_length=255, primary_key=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['empress.Task'])),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('retinue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['empress.Server'])),
            ('state', self.gf('django.db.models.fields.CharField')(default='PENDING', max_length=255)),
            ('data', self.gf('django.db.models.fields.TextField')(default='')),
            ('ex_data', self.gf('django.db.models.fields.TextField')(default='')),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 14, 0, 0))),
            ('date_archived', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal(u'empress', ['EmpressMission'])


    def backwards(self, orm):
        # Removing unique constraint on 'Server', fields ['ip_address', 'port']
        db.delete_unique(u'empress_server', ['ip_address', 'port'])

        # Removing unique constraint on 'EnvironmentVariable', fields ['application', 'name']
        db.delete_unique(u'empress_environmentvariable', ['application_id', 'name'])

        # Deleting model 'VirtualEnv'
        db.delete_table(u'empress_virtualenv')

        # Deleting model 'Application'
        db.delete_table(u'empress_application')

        # Deleting model 'EnvironmentVariable'
        db.delete_table(u'empress_environmentvariable')

        # Deleting model 'Server'
        db.delete_table(u'empress_server')

        # Deleting model 'HostingShip'
        db.delete_table(u'empress_hostingship')

        # Deleting model 'Task'
        db.delete_table(u'empress_task')

        # Deleting model 'EmpressMission'
        db.delete_table(u'empress_empressmission')


    models = {
        u'empress.application': {
            'Meta': {'object_name': 'Application'},
            'alias': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'project_path': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'requirements': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'vcs': ('django.db.models.fields.CharField', [], {'default': "'Subversion'", 'max_length': '255'}),
            'vcs_password': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'vcs_path': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'vcs_username': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'virtualenv': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['empress.VirtualEnv']", 'null': 'True', 'blank': 'True'}),
            'wsgi_handler': ('django.db.models.fields.CharField', [], {'default': "'django.core.handlers.wsgi:WSGIHandler()'", 'max_length': '255'})
        },
        u'empress.empressmission': {
            'Meta': {'object_name': 'EmpressMission'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'date_archived': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 14, 0, 0)'}),
            'ex_data': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.CharField', [], {'default': "'3aa18fa7-0071-41a0-8bf8-15aea78fd467'", 'max_length': '255', 'primary_key': 'True'}),
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
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 14, 0, 0)'}),
            'date_deprecated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['empress.Server']"})
        },
        u'empress.server': {
            'Meta': {'unique_together': "(('ip_address', 'port'),)", 'object_name': 'Server'},
            'applications': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['empress.Application']", 'through': u"orm['empress.HostingShip']", 'symmetrical': 'False'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_heartbeat': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {'default': '80'})
        },
        u'empress.task': {
            'Meta': {'object_name': 'Task'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'app_name': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'date_archived': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 14, 0, 0)'}),
            'ex_data': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.CharField', [], {'default': "'8a682a14-416b-4004-922d-d3ed2dcd4e63'", 'max_length': '255', 'primary_key': 'True'}),
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