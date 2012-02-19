define([
    "jquery", 
    "underscore", 
    "backbone", 
    "models/Book"
    ],
    function($, _, Backbone, Book){

        var BookFormView = Backbone.View.extend({
            el: $("body"),

            initialize: function(){
                var self = this;

                this.book = new this.model;

                this.book.bind("change", function() {
                    $("#id_title").val(this.book.title);
                    $("#id_cover_url").val(this.book.image_url);
                    $("#id_authors").val(this.book.authors.author.name);
                    if (this.book.series_works.series_work) {
                    	$("#id_series").val(this.book.series_works.series_work.series.title);
                    	$("#id_series_num").val(this.book.series_works.series_work.user_position);
                    }
                    //$("#id_tags").val(this.book.title);
                    $("#id_isbn10").val(this.book.isbn);
                    $("#id_isbn13").val(this.book.isbn13);
                    $("#id_description").val(strip(this.book.description));
                })
            },

            events: {
                "submit #form_search_book": "search"
            },

            search: function(event) {
                this.book.search_goodreads($("#id_isbn").val());
                return false;

            }
        });

    return BookFormView;
});