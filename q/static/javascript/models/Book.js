define(["underscore", "backbone", "backbone-tastypie"],
    function() {

    var Book = Backbone.Model.extend({
        initialize: function() {
        	this.url = "/api/v2/books/book/?format=json";
        	return false;

        },

        search_goodreads: function(isbn) {
            this.url = "/api/v2/books/goodreads/?format=json&isbn="+isbn;
            this.fetch();
            return false;
        }
    });
    return Book;
});
