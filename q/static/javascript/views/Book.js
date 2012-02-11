define(["jquery", "underscore", "backbone-0.9.1", "models/Book"],
    function($, _, Backbone, Book){

        var PopulateBookForm = Backbone.View.extend({
            el: $("body"),

            initialize: function(){
                console.log("INIT!!");
                Book.bind("change", function() {
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
    return PopulateBookForm;
});