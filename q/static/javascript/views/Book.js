define([
    "jquery", 
    "underscore", 
    "backbone", 
    "models/Book/Book",
    "collections/authors"
    ],
    function($, _, Backbone, Book, AuthorCollection){

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
            
            _get_authors: function(event) {
            	console.log(event);
            	return false;
            	this.author_uri = event.attributes.resource_uri;
            	
            	this.book = new Book();

            	this.book.set({
            		title: $("#id_title").val(),
            		cover_url: $("#id_cover_url").val(),
            		authors: [this.author_uri],
            		isbn13: $("#id_isbn13").val(),
            		isbn10: $("#id_isbn10").val(),
            		description: $("#id_description").val()
            	});
            	
            	this.book.save();
            	
            },
            add_book: function(event) {
            	
            	var firstname = $("#id_authors").val().split(" ")[0];
            	var lastname = $.trim($("#id_authors").val().replace(firstname,""));
            	
            	this.authors = new AuthorCollection();
            	this.authors.bind("reset", this._get_authors);
            	this.authors.fetch({data: {"firstname": firstname, "lastname": lastname}});

            	return false;
            }
        });

    return BookFormView;
});