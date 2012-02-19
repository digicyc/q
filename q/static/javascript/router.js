// Filename: router.js
define([
  'jquery',
  'underscore',
  'backbone',
  'views/Book',
  'views/RecentBooks'
], function($, _, Backbone, BookFormView, RecentBooks ){



  var AppRouter = Backbone.Router.extend({
    routes: {
      // Define some URL routes

      '/add-book': 'showAddBooks',
      
      // Default
      '*actions': 'defaultAction'
    },

    showAddBooks: function(){
      AddBookView.render();
    },
    defaultAction: function(actions){
      // We have no matching route, lets display the home page 
      //mainHomeView.render();
      RecentBooks.render();

    }
  });

  var initialize = function(){
    var app_router = new AppRouter;
    Backbone.history.start();
  };
  return { 
    initialize: initialize
  };
});