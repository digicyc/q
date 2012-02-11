var buildBookView = function(book_model, book_controller){
    var base = document.createElement('div');
    var bookEl = document.createElement('div');

    base.appendChild(bookEl);

    var render = function() {
        bookEl.innerHTML = _.template('bookTemplate', {src: book_model.getSrc()});
    }

    book_model.addSubscriber(render);

    var show = function() {
        bookEl.style.display  = '';

    }

    var hide = function(){
        bookEl.style.display  = 'none';
    }

    return{
        showView: show,
        hideView: hide
    }
}