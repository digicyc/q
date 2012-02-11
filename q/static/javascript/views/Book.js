define(["jquery", "underscore", "backbone", "models/Book"],
    function($, _, bb, Book){

        var PopulateBookFormView = Backbone.View.extend({
            el: $("body"),

            initialize: function(){
                console.log("INIT!!");
                this.book = new Book();
                this.book.bind("change", function() {
                    $("#id_title").val(book.get("title"));
                });
            },

            events: {
                "submit #form_search_book": "search"
            },

            search: function(event) {
                console.log("n shit");
                console.log(event);
                //this.model.search_goodreads($("#id_isbn").val());

            }
        });
    return PopulateBookFormView;
});