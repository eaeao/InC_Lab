from django import template
from django.utils.datetime_safe import datetime

from inc.itembank.models import TYPE_IN_QUESTION_CHOICES, TestpaperResult

register = template.Library()

@register.filter
def array_item(array,index):
    return array[index]

@register.filter
def set_menu_title(menu,lang=''):
    if lang == "en" : return menu.title_en
    elif lang == "jp" : return menu.title_jp
    return menu.title

@register.filter
def get_url_lang(url,lang=None):
    if lang :
        return "%s?lang=%s"%(url,lang)
    return url

@register.filter
def set_language(keyword,lang=''):
    index = 0
    if lang == "en" : index = 1
    elif lang == "jp" : index = 2

    language_pack = {
        "번호": ['번호', 'No.', '番号']
        ,"첨부": ['첨부', 'Files', 'Files']
        , "게시판": ['게시판', 'Board', 'Board']
        , "제목": ['제목', 'Title', 'タイトル']
        , "작성자": ['작성자', 'Name', '投稿者']
        , "작성일": ['작성일', 'Date', '作成日']
        , "조회수": ['조회수', 'Hits', 'ヒット']
        , "다음": ['다음', 'Next', '次の']
        , "이전": ['이전', 'Prev.', '前の']
        , "글쓰기": ['글쓰기', 'Write', 'ライティング']

        , "마이페이지":['마이페이지','My Page','私のページ']
        , "관리자 페이지": ['관리자 페이지', 'Admin Page', '管理ページ']
        , "로그아웃": ['로그아웃', 'Logout', 'ログアウト']
        , "로그인": ['로그인', 'Login', 'ログイン']
        , "연구실 소식": ['연구실 소식', 'Lab. News', '研究室ニュース']
        , "InC의 연구분야": ['InC의 연구분야', 'Research Info.', '分野別教育研究案内']
        , "공지사항": ['공지사항', 'Notice', 'お知らせ']
        , "교육 동향": ['교육 동향', 'Educational Trends', '教育の動向']
        #   토론방
    }
    return language_pack[keyword][index]

@register.filter
def get_type_icon(src):
    if any(ext in src for ext in [".zip"]) :
        return "xi-file-zip"
    elif any(ext in src for ext in [".hwp",".doc",".docx",".pdf"]) :
        return "xi-file-text"
    elif any(ext in src for ext in [".jpg", ".JPG", ".png", ".PNG",".gif",".GIF",".bmp",".BMP"]):
        return "xi-file-image"
    else :
        return "xi-file"

@register.filter
def time_diff(date):
    now = datetime.now()
    timediff = now - date
    timediff = timediff.total_seconds()
    if timediff > 259200:
        return date.strftime('%y-%m-%d')
    elif timediff > 86400:
        return str(int(timediff / 3600 / 24)) + "일 전"
    elif timediff > 3600:
        return str(int(timediff / 3600)) + "시간 전"
    elif timediff > 60:
        return str(int(timediff / 60)) + "분 전"
    else:
        return "방금 전"

@register.filter
def get_type_color(type):
    if type == TYPE_IN_QUESTION_CHOICES[0][0] :
        return "#e74c3c"
    elif  type == TYPE_IN_QUESTION_CHOICES[1][0] :
        return "#3498db"
    elif  type == TYPE_IN_QUESTION_CHOICES[2][0] :
        return "#2ecc71"
    elif  type == TYPE_IN_QUESTION_CHOICES[3][0] :
        return "#e67e22"
    elif  type == TYPE_IN_QUESTION_CHOICES[4][0] :
        return "#34495e"
    else :
        return "#95a5a6"

@register.filter
def get_testpaper_results(testpaper,user):
    if user != None :
        return TestpaperResult.objects.filter(user=user,testpaper=testpaper)
    return TestpaperResult.objects.filter(testpaper=testpaper)

@register.filter
def get_last_line(arg1):
    tmp = arg1.split('\n')
    return tmp[-1]

@register.filter
def get_diff_msg(msg,exec):
    if msg == exec : return ""
    else : return msg