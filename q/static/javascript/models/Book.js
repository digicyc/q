var Book = Backbone.Model.extend({
    initialize: function() {
        console.log('init');
    },

    search_goodreads: function(isbn) {
        console.log(isbn);
        this.url = "/api/v2/books/goodreads/?format=json&isbn="+isbn;
        this.fetch();
        console.log(this);
    }
});
