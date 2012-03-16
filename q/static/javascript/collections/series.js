define([
  'jquery',
  'underscore',
  'backbone',
  "tastypie",
  "models/book/series"
], function($, _, Backbone, tastypie, Series){
  var SeriesCollection = Backbone.Collection.extend({
    url : "/api/v2/books/series/?format=json",
    model: Series
  });

  return SeriesCollection;
});
