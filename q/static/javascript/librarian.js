var Book;
Book = (function() {
    function Book(url, isbn) {
        this.url = url;
        this.isbn = isbn;
        $.ajax(this.url, {
            dataType: "json",
            data: {
                isbn: this.isbn,
                type: "GET"
            },
            success: function(data) {
                alert("Success");
                this.data = data;
                return $.extend(self, data.objects[0]);
            }
        });
    }
    return Book;
})();
