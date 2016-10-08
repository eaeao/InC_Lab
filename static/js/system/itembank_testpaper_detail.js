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

$(document).ready(function() {
    $("#a_header_nav_btn_testpapers").addClass("active");

    $(".p_itembank_testpaper_detail_contents_text").each(function(i, e){
        $(e).html($(e).html().replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/\n/g, "<br />").replace(/\t/g, "&nbsp;&nbsp;&nbsp;&nbsp;"));
    });

    $(".span_itembank_testpaper_detail_contents_content").each(function(i, e){
        $(e).html($(e).html().replace(/ /g, '&nbsp;').replace(/</g, "&lt;").replace(/>/g, "&gt;"));
    });

    $(".pre_itembank_testpaper_detail_contents_code code").each(function(i, e){
        $(e).html($(e).html().replace(/</g, "&lt;").replace(/>/g, "&gt;"));
    });

    hljs.initHighlightingOnLoad();
    $('pre code').each(function(i, block) {
        hljs.highlightBlock(block);
    });

});