# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Book.author'
        db.delete_column('ebooks_book', 'author_id')

        # Deleting field 'Book.isbn'
        db.delete_column('ebooks_book', 'isbn')

        # Adding field 'Book.metarating'
        db.add_column('ebooks_book', 'metarating', self.gf('django.db.models.fields.FloatField')(default=0.0), keep_default=False)

        # Adding field 'Book.rating'
        db.add_column('ebooks_book', 'rating', self.gf('django.db.models.fields.FloatField')(default=0.0), keep_default=False)

        # Adding field 'Book.isbn10'
        db.add_column('ebooks_book', 'isbn10', self.gf('django.db.models.fields.CharField')(db_index=True, default='', max_length=20, blank=True), keep_default=False)

        # Adding field 'Book.isbn13'
        db.add_column('ebooks_book', 'isbn13', self.gf('django.db.models.fields.CharField')(db_index=True, default='', max_length=20, blank=True), keep_default=False)

        # Adding field 'Book.gid'
        db.add_column('ebooks_book', 'gid', self.gf('django.db.models.fields.CharField')(db_index=True, default='', max_length=20, blank=True), keep_default=False)

        # Adding field 'Book.description'
        db.add_column('ebooks_book', 'description', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)

        # Adding field 'Book.is_physical'
        db.add_column('ebooks_book', 'is_physical', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Book.is_ebook'
        db.add_column('ebooks_book', 'is_ebook', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Book.checked_out'
        db.add_column('ebooks_book', 'checked_out', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True), keep_default=False)

        # Adding M2M table for field authors on 'Book'
        db.create_table('ebooks_book_authors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('book', models.ForeignKey(orm['ebooks.book'], null=False)),
            ('author', models.ForeignKey(orm['ebooks.author'], null=False))
        ))
        db.create_unique('ebooks_book_authors', ['book_id', 'author_id'])


    def backwards(self, orm):
        
        # Adding field 'Book.author'
        db.add_column('ebooks_book', 'author', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['ebooks.Author']), keep_default=False)

        # Adding field 'Book.isbn'
        db.add_column('ebooks_book', 'isbn', self.gf('django.db.models.fields.CharField')(blank=True, default=0, max_length=30, db_index=True), keep_default=False)

        # Deleting field 'Book.metarating'
        db.delete_column('ebooks_book', 'metarating')

        # Deleting field 'Book.rating'
        db.delete_column('ebooks_book', 'rating')

        # Deleting field 'Book.isbn10'
        db.delete_column('ebooks_book', 'isbn10')

        # Deleting field 'Book.isbn13'
        db.delete_column('ebooks_book', 'isbn13')

        # Deleting field 'Book.gid'
        db.delete_column('ebooks_book', 'gid')

        # Deleting field 'Book.description'
        db.delete_column('ebooks_book', 'description')

        # Deleting field 'Book.is_physical'
        db.delete_column('ebooks_book', 'is_physical')

        # Deleting field 'Book.is_ebook'
        db.delete_column('ebooks_book', 'is_ebook')

        # Deleting field 'Book.checked_out'
        db.delete_column('ebooks_book', 'checked_out_id')

        # Removing M2M table for field authors on 'Book'
        db.delete_table('ebooks_book_authors')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'ebooks.author': {
            'Meta': {'object_name': 'Author'},
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'ebooks.book': {
            'Meta': {'object_name': 'Book'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['ebooks.Author']", 'symmetrical': 'False'}),
            'checked_out': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'gid': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '20', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_ebook': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_physical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isbn10': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '20', 'blank': 'True'}),
            'isbn13': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '20', 'blank': 'True'}),
            'metarating': ('django.db.models.fields.FloatField', [], {}),
            'published_year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rating': ('django.db.models.fields.FloatField', [], {}),
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
