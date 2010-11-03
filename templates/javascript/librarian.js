(function($) {
	$.fn.editInPlace = function(options) {
		var self = this;

		/* default variables */
		// var options = $.extend({
		//
		// 		}, options);

		self.each(function() {
			$(this).prepend('<span class="edit-icon">edit</span>');

			$(this).click(function() {
				$(this).find('.edit-icon').remove();

				var revert = [];
				revert.info = $(this).html();
				revert.tag = $(this).get(0).tagName;
                title_id = $(this).attr('id').split('_')
				revert.title = title_id[0]
                revert.book_id = title_id[1]

				var textarea = '<div style="margin:0 0 20px 0"><textarea rows="10" cols="60">' + revert.info + '</textarea>';
				var button = '<div><input type="button" value="Update" class="saveButton" /> OR <input type="button" value="Cancel" class="cancelButton" /></div></div>';

				$(this).after(textarea + button).remove();

				$('.saveButton').click(function(){
					saveChanges(this, revert.title, revert.tag, revert.info, revert.book_id, false);
				});
				$('.cancelButton').click(function(){
					saveChanges(this, revert.title, revert.tag, revert.info, revert.book_id, true);
				});
			});
		});

		function saveChanges(el, title, tag, info, book_id, cancel) {
			if(!cancel) {
                var old_info = info;
                info = $(el).parent().siblings(0).val();
				var ajaxData = 'info=' + info + '&name=' + title;

				$.ajax({
					type: 'POST',
					url: '/books/api/change_attribute/'+book_id+"/",
					data: ajaxData,
					success: editSuccess
				});
			}
			else { var info = info; }

			$(el).parent().parent().after('<' + tag + ' class="edited" id="' + title + '">' + info + '</' + tag +'>').remove();
		}

		function editSuccess() {
			alert('edit successful');
		}

	}
})(jQuery);


$(document).ready(function(){
	$(".editable").editInPlace();
});
