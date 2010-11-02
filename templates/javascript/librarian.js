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
				revert.title = $(this).attr('id');
				
				var textarea = '<div style="margin:0 0 20px 0"><textarea rows="10" cols="60">' + revert.info + '</textarea>';
				var button = '<div><input type="button" value="Update" class="saveButton" /> OR <input type="button" value="Cancel" class="cancelButton" /></div></div>';
			
				$(this).after(textarea + button).remove();
				
				$('.saveButton').click(function(){
					saveChanges(this, revert.title, revert.tag, false);
				});
				$('.cancelButton').click(function(){
					saveChanges(this, revert.title, revert.tag, revert.info);
				});
			});
		});
		
		function saveChanges(el, title, tag, cancel) {
			if(!cancel) {
				var info = $(el).parent().siblings(0).val();
				var ajaxData = 'info=' + $(el).parent().siblings(0).val() + '&name=' + title;
				
				$.ajax({
					type: 'POST',
					url: '/edit-link/',
					data: ajaxData,
					success: editSuccess
				});
			}
			else { var info = cancel; }
			
			$(el).parent().parent().after('<' + tag + ' class="edited" id="' + title + '">' + info + '</' + tag +'>').remove();
		}
		
		function editSuccess() {
			alert('edit successful')
		}

	}
})(jQuery);


$(document).ready(function(){
	$(".editable").editInPlace();
});