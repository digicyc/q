define([
  'jquery',
  'underscore',
  'backbone',
  "tastypie",
  'models/RecentBooks/RecentBooksModel'
], function($, _, Backbone, tastypie, RecentBooksModel){
  var booksCollection = Backbone.Collection.extend({
    url : "/api/v2/books/book/?format=json&order_by=-id",
    model: RecentBooksModel
  });

  return booksCollection;
});