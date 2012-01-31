
function Book(url, isbn) {
    this.url = url;
    this.isbn = isbn;
    $.ajax(this.url, {
        dataType: "json",
        data: {
            isbn: this.isbn,
            type: "GET"
        },
        async: false,
        success: function(data) {
            console.log(data)
            populate(data.objects[0]);
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


function populate(book) {
    $("#id_title").val(book.title);
    $("#id_cover_url").val(book.image_url);
    $("#id_authors").val(book.authors.author.name);
    $("#id_series").val(book.series_works.series_work.series.title);
    console.log(book.series_works.series_work.user_position);
    $("#id_series_num").val(book.series_works.series_work.user_position);
    $("#id_title").val(book.title);
    $("#id_isbn10").val(book.isbn);
    $("#id_isbn13").val(book.isbn13);
    $("#id_description").val(strip(book.description));

}