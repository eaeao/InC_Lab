import re
import json
import urllib.request
from django import template
from django.utils.datetime_safe import datetime
#from mtranslate import translate
#from googleapiclient.discovery import build

from inc.itembank.models import TYPE_IN_QUESTION_CHOICES, TestpaperResult

register = template.Library()


@register.filter
def array_item(array,index):
    return array[index]


@register.filter
def set_menu_title(menu,lang=''):
    if lang == "en" : return menu.title_en
    elif lang == "ja" : return menu.title_jp
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
    elif lang == "ja" : index = 2

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
        , "더보기": ['더보기', 'More', 'もっと']

        , "마이페이지":['마이페이지','My Page','私のページ']
        , "관리자 페이지": ['관리자 페이지', 'Admin Page', '管理ページ']
        , "로그아웃": ['로그아웃', 'Logout', 'ログアウト']
        , "로그인": ['로그인', 'Login', 'ログイン']
        , "연구실 소식": ['연구실 소식', 'Lab. News', '研究室ニュース']
        , "InC의 연구분야": ['InC의 연구분야', 'Research Info.', '分野別教育研究案内']
        , "공지사항": ['공지사항', 'Notice', 'お知らせ']
        , "교육 동향": ['교육 동향', 'Educational Trends', '教育の動向']
        , "최근 업데이트":['최근 업데이트','Recent updates','最近更新さ']
        , "개인정보처리방침":['개인정보처리방침','Privacy Policy','個人情報の処理方針']
        , "저작자 표시":['저작자 표시','Attribution','表示']
        , "비영리": ['비영리', 'Noncommercial', '非営利']
        , "동일조건변경허락": ['동일조건변경허락', 'Share Alike', '継承']
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
    if type(user) is dict:
        return TestpaperResult.objects.filter(email=user['email'], testpaper=testpaper)
    elif user :
        return TestpaperResult.objects.filter(user=user, testpaper=testpaper)
    return TestpaperResult.objects.filter(testpaper=testpaper)


@register.filter
def get_last_line(arg1):
    tmp = arg1.split('\n')
    return tmp[-1]


@register.filter
def get_diff_msg(msg,exec):
    if msg == exec : return ""
    else : return msg


@register.filter
def check_jongsung(test_keyword):
    BASE_CODE, CHOSUNG, JUNGSUNG = 44032, 588, 28
    JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

    split_keyword_list = list(test_keyword)

    keyword = split_keyword_list[-1]
    if re.match('.*[ㄱ-ㅎㅏ-ㅣ가-힣]+.*', keyword) is not None:
        char_code = ord(keyword) - BASE_CODE
        char1 = int(char_code / CHOSUNG)
        char2 = int((char_code - (CHOSUNG * char1)) / JUNGSUNG)
        char3 = int((char_code - (CHOSUNG * char1) - (JUNGSUNG * char2)))
        return char3
    return None


@register.filter
def translate_language(text, target):
    if target :
        try :
            client_id = "WimulHGKkwGKjgui9RzG"
            client_secret = "7TX3BBHzPk"
            encText = urllib.parse.quote(text)
            data = "source=ko&target="+ target +"&text=" + encText
            url = "https://openapi.naver.com/v1/language/translate"
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id", client_id)
            request.add_header("X-Naver-Client-Secret", client_secret)
            response = urllib.request.urlopen(request, data=data.encode("utf-8"))
            rescode = response.getcode()
            if (rescode == 200):
                response_body = response.read().decode('utf-8')
                return json.loads(response_body)['message']['result']['translatedText']
        except Exception as e :
            pass
    return text

# @register.filter
# def translate_language(text, target):
#     if target :
#         return translate(text, target)
#     else :
#         return text

# @register.filter
# def google_translate(text, target):
#     if target :
#         service = build('translate', 'v2',
#                         developerKey='AIzaSyCW29vKIqnHaiuErnMQMgAeHQ8mAR6xvwE')
#         return service.translations().list(
#             target=target,
#             q=text
#         ).execute()['translations'][0]['translatedText']
#     else :
#         return text