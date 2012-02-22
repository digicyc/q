define([
  'jquery',
  'underscore',
  'backbone',
  "tastypie",
  'models/book/author'
], function($, _, Backbone, tastypie, Author){
  var AuthorCollection = Backbone.Collection.extend({
    url : "/api/v2/books/author/?format=json",
    model: Author
  });

  return AuthorCollection;
});
