
function get_book_info(url, isbn) {
    this.url = url;
    this.isbn = isbn;
    $.ajax(this.url, {
        dataType: "json",
        data: {
            isbn: this.isbn,
            type: "GET"
        },
        success: function(data) {
            _populate(data.objects[0]);
            return false;
        }
    });
}

function put_book_info(url){
    this.url = url;

    $.ajax(this.url, {
        dataType: "json",
        type: "POST",
        data: {
            title: $("#id_title").val(),
            cover_url: $("#id_cover_url").val(),
            //authors: $("#id_authors").val(),
            //series: $("#id_series").val(),
            series_num: $("#id_series_num").val(),
            tags: $("#id_tags").val(),
            isbn10: $("#id_isbn10").val(),
            isbn13: $("#id_isbn13").val(),
            description: $("#id_description").val()
        },
        success: function(data) {
            console.log(data);
            return false;
        }
    });
}

function strip(html)
{
    var tmp = document.createElement("DIV");
    tmp.innerHTML = html;
    return tmp.textContent||tmp.innerText;
}


function _populate(book) {
    $("#id_title").val(book.title);
    $("#id_cover_url").val(book.image_url);
    $("#id_authors").val(book.authors.author.name);
    if (book.series_works.series_work) {
    $("#id_series").val(book.series_works.series_work.series.title);
    $("#id_series_num").val(book.series_works.series_work.user_position);
    }
    //$("#id_tags").val(book.title);
    $("#id_isbn10").val(book.isbn);
    $("#id_isbn13").val(book.isbn13);
    $("#id_description").val(strip(book.description));

}