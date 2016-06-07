/**
 * Created by 박동혁 on 2016-05-24.
 */

var form_content = {
    'type':'content'
    ,'title':"내용"
    ,'body_html':'<div class="controls"><input type="hidden" name="type" value="content"><input class="form-control input_itembank_write_left_content" type="text" name="content" onkeyup="makeExample()" placeholder="내용을 입력해주세요."></div>'
    ,'is_moveable':true
    ,'is_flexible':true
    ,'extra_btns':''
    ,'callback':null
};
var form_image = {
    'type':'image'
    ,'title':"이미지"
    ,'body_html':'<div class="controls"><input type="hidden" name="type" value="image"><input class="form-control input_itembank_write_left_image" type="file" accept="image/*" name="image" onchange="makeExample()"></div>'
    ,'is_moveable':true
    ,'is_flexible':true
    ,'extra_btns':''
    ,'callback':null
};
var form_text = {
    'type':'text'
    ,'title':"보기지문"
    ,'body_html':'<div class="controls"><input type="hidden" name="type" value="text"><textarea class="form-control input_itembank_write_left_text" onkeyup="makeExample()" name="text" placeholder="지문을 입력해주세요."></textarea></div>'
    ,'is_moveable':true
    ,'is_flexible':true
    ,'extra_btns':''
    ,'callback':null
};
var form_code = {
    'type':'code'
    ,'title':"프로그래밍 지문"
    ,'body_html':'<div class="controls"><input type="hidden" name="type" value="code"><textarea class="form-control input_itembank_write_left_code" onkeyup="makeExample()" name="code" placeholder="코드를 입력해주세요."></textarea></div>'
    ,'is_moveable':true
    ,'is_flexible':true
    ,'extra_btns':''
    ,'callback':null
};
var form_answer_text = {
    'type':'answer_text'
    ,'title':"단답식 답안"
    ,'body_html':'<div class="controls"><input type="hidden" name="type" value="answer_text"><input class="form-control input_itembank_write_left_answer_text" type="text" name="answer_text" onkeyup="makeExample()" placeholder="답을 입력해주세요."></div>'
    ,'is_moveable':true
    ,'is_flexible':true
    ,'extra_btns':''
    ,'callback':null
};
var form_answer_textarea = {
    'type':'answer_textarea'
    ,'title':"서술식 답안"
    ,'body_html':'<div class="controls"><input type="hidden" name="type" value="answer_textarea"><textarea class="form-control input_itembank_write_left_answer_textarea" onkeyup="makeExample()" name="answer_textarea" placeholder="답을 입력해주세요."></textarea></div>'
    ,'is_moveable':true
    ,'is_flexible':false
    ,'extra_btns':''
    ,'callback':null
};
var form_answer_choice = {
    'type':'answer_choice'
    ,'title':"객관식 답안"
    ,'body_html':'<div class="controls div_itembank_write_left_answer_choice"><input type="hidden" name="type" value="answer_choice"><ul>'
    +'<li class="li_itembank_write_left_answer_choice"><input type="radio" name="answer_choice_radio" value="" class="input_itembank_write_left_answer_choice_radio"><input class="form-control input-sm input_itembank_write_left_answer_choice" type="text" name="answer_choice" onkeyup="makeExample();setRadioValue(this);" placeholder="답을 입력해주세요."><i class="xi-trash i_itembank_write_left_answer_choice_remove" onclick="removeChoiceLine(this)"></i></li>'
    +'<li class="li_itembank_write_left_answer_choice"><input type="radio" name="answer_choice_radio" value="" class="input_itembank_write_left_answer_choice_radio"><input class="form-control input-sm input_itembank_write_left_answer_choice" type="text" name="answer_choice" onkeyup="makeExample();setRadioValue(this);" placeholder="답을 입력해주세요."><i class="xi-trash i_itembank_write_left_answer_choice_remove" onclick="removeChoiceLine(this)"></i></li>'
    +'<li class="li_itembank_write_left_answer_choice"><input type="radio" name="answer_choice_radio" value="" class="input_itembank_write_left_answer_choice_radio"><input class="form-control input-sm input_itembank_write_left_answer_choice" type="text" name="answer_choice" onkeyup="makeExample();setRadioValue(this);" placeholder="답을 입력해주세요."><i class="xi-trash i_itembank_write_left_answer_choice_remove" onclick="removeChoiceLine(this)"></i></li>'
    +'<li class="li_itembank_write_left_answer_choice"><input type="radio" name="answer_choice_radio" value="" class="input_itembank_write_left_answer_choice_radio"><input class="form-control input-sm input_itembank_write_left_answer_choice" type="text" name="answer_choice" onkeyup="makeExample();setRadioValue(this);" placeholder="답을 입력해주세요."><i class="xi-trash i_itembank_write_left_answer_choice_remove" onclick="removeChoiceLine(this)"></i></li>'
    +'</ul></div>'
    ,'is_moveable':true
    ,'is_flexible':false
    ,'extra_btns':'<i class="xi-plus i_itembank_write_left_btns_addchoice" onclick="addChoiceLine(this)"></i>'
    ,'callback':null
};

var line_no = 0;

function addLine(arg){
    var moveable = 'ui-state-disabled';
    var flexible = '';
    if (arg.is_moveable == true) moveable = 'ui-state-default';
    if (arg.is_flexible == true) flexible = '<i class="xi-arrows-h i_itembank_write_left_btns_extend active" onclick="widthLine('+line_no+')"></i>';

    var line_html = '<li class="li_itembank_write_left_list_line '+moveable+'" type="'+arg.type+'" id="li_itembank_write_left_list_line_'+line_no+'"><i class="xi-bars btn_itembank_write_left_list_line_move"></i><div><label class="control-label">'
        +arg.title
        +'</label><div class="div_itembank_write_left_btns">'
        +arg.extra_btns
        +flexible
        +'<i class="xi-trash i_itembank_write_left_btns_remove" onclick="removeLine('+line_no+')"></i>'
        +'</div>'
        +arg.body_html
        +'</div></li>';
    line_no++;
    if (typeof arg.func_name === "function") $("#ul_itembank_write_left_list").append(line_html).then(arg.callback());
    else $("#ul_itembank_write_left_list").append(line_html);
    makeExample();
}

function removeLine(no){
    var r = confirm("정말 삭제하시겠습니까?");
    if (r == true) {
        $("#li_itembank_write_left_list_line_"+no).remove();
        makeExample();
    }
}

function widthLine(no){
    var btn_extend = $("#li_itembank_write_left_list_line_"+no+" .i_itembank_write_left_btns_extend");
    if(btn_extend.hasClass("active")) btn_extend.removeClass("active");
    else btn_extend.addClass("active");
    makeExample();
}

function addChoiceLine(e){
    var line_html = '<li class="li_itembank_write_left_answer_choice"><input type="radio" name="answer_choice_radio" value="0" class="input_itembank_write_left_answer_choice_radio"><input class="form-control input-sm input_itembank_write_left_answer_choice" type="text" name="answer_choice" onkeyup="makeExample();setRadioValue(this);" placeholder="답을 입력해주세요."><i class="xi-trash i_itembank_write_left_answer_choice_remove" onclick="removeChoiceLine(this)"></i></li>';
    $(e).parent().siblings('.div_itembank_write_left_answer_choice').children('ul').append(line_html);
    makeExample();
    setChkbox();
}

function removeChoiceLine(e){
    $(e).parent().remove();
    makeExample();
}

function setRadioValue(e){
    $(e).parent().contents().find('.input_itembank_write_left_answer_choice_radio').val($(e).val());
}

function makeExample(){
    var str_body = "";
    var ele_no = -1;
    $("#ul_itembank_write_left_list").children().each(function (i, e) {
        var input_type = $(e).attr("type");
        var input_ele_value = "";
        var input_ele_inline = "";
        ele_no++;
        if(input_type == "content"){
            if(!$(e).contents().find(".i_itembank_write_left_btns_extend").hasClass("active")) input_ele_inline = "span_inline";
            input_ele_value = $(e).contents().find(".input_itembank_write_left_content").val().replace(/ /g, '&nbsp;').replace(/</g, "&lt;").replace(/>/g, "&gt;");
            if(input_ele_value){
                str_body += "<span class='span_itembank_write_right_content ele_"+ele_no+" "+input_ele_inline+"'>"+input_ele_value+"</span>";
            } else {
                str_body += "<span class='span_itembank_write_right_content ele_"+ele_no+" "+input_ele_inline+"'>내용을 입력해주세요.</span>";
            }
        }else if(input_type == "image"){
            if(!$(e).contents().find(".i_itembank_write_left_btns_extend").hasClass("active")) input_ele_inline = "p_inline";
            input_ele_value = $(e).contents().find(".input_itembank_write_left_image")[0].files[0];
            if(input_ele_value){
                str_body += "<p class='p_itembank_write_right_image uploaded ele_"+ele_no+" "+input_ele_inline+"'><img class='img_itembank_write_right_image'></p>";
                readURL(ele_no,input_ele_value);
            } else {
                str_body += "<p class='p_itembank_write_right_image ele_"+ele_no+" "+input_ele_inline+"'>이미지 없음</p>";
            }
        }else if(input_type == "text"){
            if(!$(e).contents().find(".i_itembank_write_left_btns_extend").hasClass("active")) input_ele_inline = "p_inline";
            input_ele_value = $(e).contents().find(".input_itembank_write_left_text").val().replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/\n/g, '<br />').replace(/\t/g, '&nbsp;&nbsp;&nbsp;&nbsp;');
            if(input_ele_value){
                str_body += "<p class='p_itembank_write_right_text uploaded ele_"+ele_no+" "+input_ele_inline+"'>"+input_ele_value+"</p>";
            } else {
                str_body += "<p class='p_itembank_write_right_text ele_"+ele_no+" "+input_ele_inline+"'>보기지문 없음</p>";
            }
        }else if(input_type == "code"){
            if(!$(e).contents().find(".i_itembank_write_left_btns_extend").hasClass("active")) input_ele_inline = "p_inline";
            input_ele_value = $(e).contents().find(".input_itembank_write_left_code").val().replace(/</g, "&lt;");
            if(input_ele_value){
                str_body += "<pre class='pre_itembank_write_right_code uploaded ele_"+ele_no+" "+input_ele_inline+"'><code class='python`'>"+input_ele_value+"</code></pre>";
            } else {
                str_body += "<p class='pre_itembank_write_right_code ele_"+ele_no+" "+input_ele_inline+"'>코드 없음</p>";
            }
        }else if(input_type == "answer_text"){
            if(!$(e).contents().find(".i_itembank_write_left_btns_extend").hasClass("active")) input_ele_inline = "input_inline";
            input_ele_value = $(e).contents().find(".input_itembank_write_left_answer_text").val().replace(/</g, "&lt;").replace(/>/g, "&gt;");
            str_body += "<input type='text' class='form-control input_itembank_write_right_answer_text ele_"+ele_no+" "+input_ele_inline+"' value='"+input_ele_value+"' placeholder='답을 입력해주세요.'>";
        }else if(input_type == "answer_textarea"){
            input_ele_value = $(e).contents().find(".input_itembank_write_left_answer_textarea").val().replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/\n/g, '<br />').replace(/\t/g, '&nbsp;&nbsp;&nbsp;&nbsp;');
            str_body += "<textarea class='form-control input_itembank_write_right_answer_textarea ele_"+ele_no+"' placeholder='답을 입력해주세요.'>"+input_ele_value+"</textarea>";
        }else if(input_type == "answer_choice"){
            $(e).contents().find(".input_itembank_write_left_answer_choice").each(function (i, e) {
                input_ele_value = $(e).val()
                if(input_ele_value){
                    str_body += '<div class="div_itembank_write_right_item"><input type="radio" name="radio_ex"> '+input_ele_value+'</div>';
                } else {
                    str_body += '<div class="div_itembank_write_right_item"><input type="radio" name="radio_ex">답지보기</div>';
                }
            });
        }
    });
    $("#div_itembank_write_right_body").html(str_body);
    setChkbox();
    setCodeView();
}

function setCodeView(){
    $(document).ready(function() {
        hljs.initHighlightingOnLoad();
        $('pre code').each(function(i, block) {
            hljs.highlightBlock(block);
        });
    });
}

function setChkbox(){
    $('input[type=radio],input[type=checkbox]').iCheck({
        checkboxClass: 'icheckbox_square-blue',
        radioClass: 'iradio_square-blue',
        increaseArea: '20%' // optional
    });
}

function readURL(no,file_src) {
    var reader = new FileReader();
    reader.onload = function (e) {
        $(".p_itembank_write_right_image.ele_"+no+" .img_itembank_write_right_image").attr("src",e.target.result);
    }
    reader.readAsDataURL(file_src);
}

$(document).delegate('textarea', 'keydown', function(e) {
    var keyCode = e.keyCode || e.which;

    if (keyCode == 9) {
        e.preventDefault();
        var start = $(this).get(0).selectionStart;
        var end = $(this).get(0).selectionEnd;

        // set textarea value to: text before caret + tab + text after caret
        $(this).val($(this).val().substring(0, start)
            + "\t"
            + $(this).val().substring(end));

        // put caret at right position again
        $(this).get(0).selectionStart =
            $(this).get(0).selectionEnd = start + 1;
    }
});
