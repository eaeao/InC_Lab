$(document).ready(function() {

    $("#a_header_nav_btn_testpapers").addClass("active");
    $('[data-toggle="tooltip"]').tooltip();

    (function() {
        $("#ul_itembank_testpaper_write_list_questions").sortable({
            items: ".li_itembank_testpaper_write_list_question",
            update: function( event, ui ) {

            }
        });
        $( "#ul_itembank_testpaper_write_list_questions" ).disableSelection();
    })();

    $("#input_itembank_testpaper_write_title").keyup(function () {
        activeSubmit();
    });

    $("#btn_itembank_testpaper_write_list_submit").click(function(){
        var testpaper_title = $("#input_itembank_testpaper_write_title").val();
        var questions_id = [];
        $("#ul_itembank_testpaper_write_list_questions .li_itembank_testpaper_write_list_question").each(function(i, ele){
            questions_id.push($(ele).attr("qid"));
        })

        $.post("/itembank/testpaper/write/",{
            "csrfmiddlewaretoken":$("#wrap > input[name=csrfmiddlewaretoken]").val(),
            "testpaper_title":testpaper_title,
            "questions_id":questions_id
        },function (data) {
            if(data=="0"||data==0){
                location.href="/itembank/";
            }
            console.log(data);
        });

    });

});

function removeLine(ele) {
    var line = $(ele).parents(".li_itembank_testpaper_write_list_question")
    line.remove();
    if( $("#ul_itembank_testpaper_write_list_questions").children(".li_itembank_testpaper_write_list_question").length < 1 ) $(".li_itembank_testpaper_write_list_question_nodata").show();
    activeSubmit();
}

function addLine(ele){
    $(".li_itembank_testpaper_write_list_question_nodata").hide();
    var question = $(ele)
    var str = '<li class="li_itembank_testpaper_write_list_question ui-state-default" qid="' +
        question.attr("qid") +
        '">' +
        question.children(".p_itembank_question_card_title").text() +
        '<p class="p_itembank_testpaper_write_list_question_panel"> <i class="xi-close" onclick="removeLine(this)"></i> </p> </li>';
    $("#ul_itembank_testpaper_write_list_questions").append(str);
    activeSubmit();
}

function activeSubmit() {
    if( $("#ul_itembank_testpaper_write_list_questions").children(".li_itembank_testpaper_write_list_question").length > 0 ){
        if( $("#input_itembank_testpaper_write_title").val() != "" ){
            $("#btn_itembank_testpaper_write_list_submit").removeAttr("disabled");
            return false;
        }
    }
    $("#btn_itembank_testpaper_write_list_submit").attr("disabled","disabled");
}