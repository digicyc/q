define([
    "jquery", 
    "underscore", 
    "backbone", 
    "models/book/book",
    "collections/authors",
    "collections/addBook",
    "collections/series"
    ],
    function($, _, Backbone, Book, AuthorCollection, AddBooksCollection, SeriesCollection){

        var BookFormView = Backbone.View.extend({
            
            el: $("body"),

            initialize: function(){
                var self = this;

                 _.bindAll(this, "populateBookForm", "search", "getSeries", "getAuthors", "saveBook");

                this.collection = new AddBooksCollection;
                this.authors = new AuthorCollection;
                this.series = new SeriesCollection;

                this.collection.on("reset", this.populateBookForm);
                this.series.on("reset", this.getAuthors);
                this.series.on("add", this.getAuthors);

                this.authors.on("reset", this.saveBook);
                this.authors.on("add", this.saveBook);

            },

            events: {
                "submit #form_search_book": "search",
                "submit #form_add_book": "getSeries"
            },
            search: function(event) {
                var isbn = $("#id_isbn").val();
                this.collection.fetch({data: { "isbn": isbn }});
                return false;
            },
            populateBookForm : function(){
                var book = this.collection.toJSON();
                $("#id_title").val(book[0].title);
                $("#id_cover_url").val(book[0].image_url);
                $("#id_authors").val(book[0].authors.join(","));
                if (book[0].series_works.series_work) {
                    $("#id_series").val(book[0].series_works.series_work.series.title);
                    $("#id_series_num").val(book[0].series_works.series_work.user_position);
                }
                $("#id_tags").val(book[0].title);
                $("#id_isbn10").val(book[0].isbn);
                $("#id_isbn13").val(book[0].isbn13);
                $("#id_description").val(strip(book[0].description));
                return false;
            },
            
            saveBook : function() {
                var authors = this.authors.toJSON();
                var series = this.series.toJSON();

                var authors_array = new Array();
                for (var i=0;i<authors.length;i++) {
                    authors_array.push(authors[i].resource_uri);
                }
                console.debug(series);
                var book = new Book();
                book.set({
                    title: $("#id_title").val(),
                    cover_url: $("#id_cover_url").val(),
                    authors: authors_array,
                    isbn13: $("#id_isbn13").val(),
                    isbn10: $("#id_isbn10").val(),
                    series: series[0].resource_uri,
                    series_num: $("#id_series_num").val(),
                    description: $("#id_description").val()
                });
                book.save();
            },

            getAuthors : function() {
                _authors = new Array();
                authors = $("#id_authors").val().split(",");
                for (var i=0;i<authors.length;i++) {
                    var firstname = authors[i].split(" ").slice(0,-1);
                    firstname = firstname.join(" ");
                    var lastname = authors[i].split(" ").slice(-1);
                    
                    _authors.push({name: "firstname__iexact", value: firstname});
                    _authors.push({name: "lastname__iexact", value: lastname});
                }
                
                this.authors.fetch({add: true, data: $.param(_authors)});
                return false;
            },
            
            getSeries : function () {
            	var s_name = $('#id_series').val();
            	this.series.fetch({add: true, data: $.param({name: s_name})})
            	return false;
            }
        });

    return new BookFormView;
});