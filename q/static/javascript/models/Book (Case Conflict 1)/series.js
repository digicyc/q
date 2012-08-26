define([
        "underscore", 
        "backbone", 
        "tastypie"
    ],
    function() {

    var Series = Backbone.Model.extend({
        url: '/api/v2/books/series/?format=json'
    });

    return Series;
});