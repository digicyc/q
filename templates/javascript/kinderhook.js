$(document).ready(function(){
    
    var QK = new QKinderHook();
    
    $('#i-own-this a').live('click', function(){
        QK.manage_ownership(this);
    });
    
});


var QKinderHook = function(){ this.init.apply(this, arguments); }
    QKinderHook.prototype = {
        init : function() {},
        manage_ownership : function(obj)
        {
            var book_id = obj.id.split('_')[1];
        
            var send_data = {'book_id':book_id}
            $.getJSON('/books/api/i_own_this_book/', send_data, function(data){
               html_out = "";
           
               if(data['ownership'])
               {
                   html_out += '<h2 class="section-title">My QR Code</h2>';
                   html_out += '<div class="qr-code"><p><a href="/books/checkout/'+data['key']+'">';
                   html_out += '<img src="'+data['ownership']['qr_code']+'" />';
                   html_out += '</a></p></div>';
                   html_out += '<div id="i-own-this" style="text-align: right; padding: 7px">';
                   html_out += '<small><a href="#" id="book_'+book_id+'">. . . I don\'t own this.</a></small>';
                   html_out += '</div>';
                } else {
                    html_out += '<div id="i-own-this-box">';
                    html_out += '<p id="i-own-this"><a href="#" id="book_'+book_id+'">i own this</a></p>';
                    html_out += '</div>';
                }

               $('#i-own-this-box').fadeOut(function(){
                   $('#i-own-this-box').html(html_out);
                   $('#i-own-this-box').fadeIn();
               });
            
            });
            return false;
            
        }
    }