// Filename: views/projects/list
define([
  'jquery',
  'underscore',
  'backbone',
  // Pull in the Collection module from above
  'collections/recentbooks',
  'text!templates/booklist.html'

], function($, _, Backbone, booksCollection, listTemplate){
  var booksListView = Backbone.View.extend({
    el: $("#recent_books"),
    initialize: function(){
        this.collection = new booksCollection;
        _.bindAll(this, "loadBind","sizeBar");
        this.collection.bind("reset", this.loadBind);
        this.collection.fetch();


    },
    loadBind: function( model ){
        var compiled_template = _.template( listTemplate ),
            collection = this.collection;
            $el = $(this.el);
            $el.html( compiled_template( { results: collection.models } ) );
            this.sizeBar();
            this.hoverItem();
    },
    hoverItem : function() {
      $('li',this.el).on({
        mouseenter : function() {
          $(this).addClass('over');
        },
        mouseleave : function() {
          $(this).removeClass('over');
        }
      });
    },
    sizeBar : function() {
      var winHeight = $(window).height();
      $(this.el).height(winHeight-140);
    }
  });
  return new booksListView;
});
