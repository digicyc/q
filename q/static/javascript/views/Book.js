define([
    "jquery", 
    "underscore", 
    "backbone", 
    "models/Book/Book"
    ],
    function($, _, Backbone, Book){

        var BookFormView = Backbone.View.extend({
            el: $("body"),

            initialize: function(){
                var self = this;

                this.book = new this.model;

                this.book.bind("change", function() {
                	this.book = this.attributes;
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
                    
                    var tmp = document.createElement("DIV");
                    tmp.innerHTML = this.book.description;
                    description = tmp.textContent||tmp.innerText;
                    
                    $("#id_description").val(description);
                    return false;
                })
            },

            events: {
                "submit #form_search_book": "search",
                "submit #form_add_book": "add_book"
            },

            search: function(event) {
                this.book.search_goodreads($("#id_isbn").val());
                return false;

            },
            add_book: function(event) {
            	this.book = new Book()
            	this.book.set({
            		title: $("#id_title").val(),
            		cover_url: $("#id_cover_url").val(),
            		//authors: $("#id_authors").val(),
            		authors: ["/api/v2/books/author/1/"],
            		isbn13: $("#id_isbn13").val(),
            		isbn10: $("#id_isbn10").val(),
            		description: $("#id_description").val()
            	});
                if ($("#id_series").val() != "") {
                	this.book.set("series", $("#id_series").val());
                	this.book.set("series_num", $("#id_series_num").val());
                }
                
                this.book.save();
            	return false;
            }
        });

    return BookFormView;
});