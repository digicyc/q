define(["underscore", "backbone-0.9.1", "backbone-tastypie-0.1"],
    function() {

    var Book = Backbone.Model.extend({
        initialize: function() {

        },

        search_goodreads: function(isbn) {
            this.url = "/api/v2/books/goodreads/?format=json&isbn="+isbn;
            this.fetch();
        }
    });
});
