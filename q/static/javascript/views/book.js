define([
    "jquery", 
    "underscore", 
    "backbone", 
    "models/book/book",
    "collections/authors",
    "collections/addBook"
    ],
    function($, _, Backbone, Book, AuthorCollection, AddBooksCollection){

        var BookFormView = Backbone.View.extend({
            
            el: $("body"),

            initialize: function(){
                var self = this;

                 _.bindAll(this, "populateBookForm", "search", "getAuthors");

                this.collection = new AddBooksCollection;
                this.authors = new AuthorCollection;

                this.collection.bind("reset", this.populateBookForm);
                this.authors.bind("reset", this.getAuthors);
            },

            events: {
                "submit #form_search_book": "search",
                "submit #form_add_book": "addBook"
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
            getAuthors : function() {
                var authors = this.authors.toJSON();

                var authors_array = new Array();
                for (var i=0;i<authors.length;i++) {
                    authors_array.push(authors[i].resource_uri);
                }
                var book = new Book();
                book.set({
                    title: $("#id_title").val(),
                    cover_url: $("#id_cover_url").val(),
                    authors: authors_array,
                    isbn13: $("#id_isbn13").val(),
                    isbn10: $("#id_isbn10").val(),
                    description: $("#id_description").val()
                });
                book.save();
            },
            search: function(event) {
                var isbn = $("#id_isbn").val();
                this.collection.fetch({data: { "isbn": isbn }});
                return false;
            },
            addBook : function() {
                _authors = new Array();
                authors = $("#id_authors").val().split(",");
                for (var i=0;i<authors.length;i++) {
                    var firstname = authors[i].split(" ")[0];
                    var lastname = $.trim(authors[i].replace(firstname,""));
                    
                    _authors.push({name: "firstname"+i+"__iexact", value: firstname});
                    _authors.push({name: "lastname"+i+"__iexact", value: lastname});
                }
                this.authors.fetch({data: $.param(_authors)});

                return false;
            }
        });

    return new BookFormView;
});