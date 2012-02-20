define([
        "underscore", 
        "backbone", 
        "tastypie"
    ],
    function() {

    var Author = Backbone.Model.extend({
        initialize: function() {
            this.url = "/api/v2/books/author/?format=json";
            return false;

        }
    });
    return Author;
});
