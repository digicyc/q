// Filename: views/projects/list
define([
  'jquery',
  'underscore',
  'backbone',
  // Pull in the Collection module from above
  'collections/books',
  'text!templates/booklist.html'

], function($, _, Backbone, booksCollection, listTemplate){
  var booksListView = Backbone.View.extend({
    el: $("#recent_books"),
    initialize: function(){
      this.collection = new booksCollection;

        _.bindAll(this, "loadBind");
        this.collection.bind("reset", this.loadBind);
        this.collection.fetch();

    },
    loadBind: function( model ){
        var compiled_template = _.template( listTemplate ),
            collection = this.collection;
            $el = $(this.el);
            $el.html( compiled_template( { results: collection.models } ) );
    }
  });
  return new booksListView;
});
