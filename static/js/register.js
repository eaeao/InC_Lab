$(document).ready(function () {

    $("#join_message").click(function(){
        var this_height = $(this).height();
        if(this_height<=120){
            $(this).css({"height":"auto","overflow":"visible"});
        }else{
            $(this).css({"height":"150px","overflow":"hidden"});
        }
    });

});