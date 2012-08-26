define([
        "underscore", 
        "backbone", 
        "tastypie"
    ],
    function() {

    var Book = Backbone.Model.extend({
        url: '/api/v2/books/book/?format=json'
    });

    return Book;
});


    //    initialize: function() {
    //         this.url = "/api/v2/books/book/?format=json";
    //         return false;
    //     },
    //     search_goodreads: function(isbn) {
    //         this.url = "/api/v2/books/goodreads/?format=json&isbn="+isbn;
    //         this.fetch();
    //     }
    // });