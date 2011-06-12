# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Book'
        db.create_table('ebooks_book', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ebooks.Author'])),
            ('isbn', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=30, blank=True)),
            ('published_year', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('update_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('cover', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, db_index=True)),
        ))
        db.send_create_signal('ebooks', ['Book'])

        # Adding model 'Format'
        db.create_table('ebooks_format', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ebook', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ebooks.Book'])),
            ('format', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('ebook_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('ebooks', ['Format'])

        # Adding unique constraint on 'Format', fields ['ebook', 'format']
        db.create_unique('ebooks_format', ['ebook_id', 'format'])

        # Adding model 'Author'
        db.create_table('ebooks_author', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal('ebooks', ['Author'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Format', fields ['ebook', 'format']
        db.delete_unique('ebooks_format', ['ebook_id', 'format'])

        # Deleting model 'Book'
        db.delete_table('ebooks_book')

        # Deleting model 'Format'
        db.delete_table('ebooks_format')

        # Deleting model 'Author'
        db.delete_table('ebooks_author')


    models = {
        'ebooks.author': {
            'Meta': {'object_name': 'Author'},
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'ebooks.book': {
            'Meta': {'object_name': 'Book'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ebooks.Author']"}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '30', 'blank': 'True'}),
            'published_year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'update_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'ebooks.format': {
            'Meta': {'unique_together': "(('ebook', 'format'),)", 'object_name': 'Format'},
            'ebook': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ebooks.Book']"}),
            'ebook_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['ebooks']
