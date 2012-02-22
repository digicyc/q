define([
  'jquery',
  'underscore',
  'backbone',
  "tastypie",
  'models/book/book'
], function($, _, Backbone, tastypie, Book){
  var AddBooksCollection = Backbone.Collection.extend({
    url : "/api/v2/books/goodreads/?format=json",
    model: Book
  });

  return AddBooksCollection;
});