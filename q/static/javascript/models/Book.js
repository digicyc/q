define(["underscore", "backbone", "backbone-tastypie"],
    function() {

    var Book = Backbone.Model.extend({
        initialize: function() {

        },

        search_goodreads: function(isbn) {
            this.url = "/api/v2/books/goodreads/?format=json&isbn="+isbn;
            this.fetch();
        }
    });
    return Book;
});
