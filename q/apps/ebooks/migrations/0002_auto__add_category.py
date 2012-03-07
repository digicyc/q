# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Category'
        db.create_table('ebooks_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('ebooks', ['Category'])

        # Adding M2M table for field books on 'Category'
        db.create_table('ebooks_category_books', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('category', models.ForeignKey(orm['ebooks.category'], null=False)),
            ('book', models.ForeignKey(orm['ebooks.book'], null=False))
        ))
        db.create_unique('ebooks_category_books', ['category_id', 'book_id'])


    def backwards(self, orm):
        
        # Deleting model 'Category'
        db.delete_table('ebooks_category')

        # Removing M2M table for field books on 'Category'
        db.delete_table('ebooks_category_books')


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
        'ebooks.category': {
            'Meta': {'object_name': 'Category'},
            'books': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['ebooks.Book']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
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
