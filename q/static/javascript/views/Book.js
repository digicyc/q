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
                $("#id_authors").val(book[0].authors.author.name);
                if (book[0].series_works.series_work) {
                    $("#id_series").val(book[0].series_works.series_work.series.title);
                    $("#id_series_num").val(book[0].series_works.series_work.user_position);
                }
                $("#id_tags").val(book[0].title);
                $("#id_isbn10").val(book[0].isbn);
                $("#id_isbn13").val(book[0].isbn13);
                $("#id_description").val(book[0].description);
                return false;
            },
            getAuthors : function() {
                var author = this.authors.toJSON();

                // Log the author object
                console.log(author);

                var book = new Book();
                book.set({
                    title: $("#id_title").val(),
                    cover_url: $("#id_cover_url").val(),
                    authors: [author.author_uri],
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
                                
                var firstname = $("#id_authors").val().split(" ")[0];
                var lastname = $.trim($("#id_authors").val().replace(firstname,""));
                this.authors.fetch({data: {"firstname": firstname, "lastname": lastname}});
                return false;
            }
        });

    return new BookFormView;
});