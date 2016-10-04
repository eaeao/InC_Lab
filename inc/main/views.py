import os
import time
from operator import itemgetter

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from inc import settings
from inc.main.models import UserProfile, Menu, Page, get_or_none, DocPaper, Board, BoardFile, BoardReply, \
    TYPE_IN_PAPER_CHOICES, DocBook, GRADE_IN_SCHOOL_CHOICES, UserSchool
from inc.main.templatetags.main_extras import set_menu_title


def main(request):
    if not request.user.id :
        return HttpResponseRedirect('/auth/login/?from=/auth/login/')
    elif not request.user.is_superuser :
        return HttpResponseRedirect('/menu/1')

    menu_icons = [
        'xi-chart-pyramid',
        'xi-lecture',
        'xi-chart-star',
        'xi-family',
        'xi-book-spread',
        'xi-tablet-pen',
        'xi-code',
        'xi-tagged-book'
    ]

    boards = BoardFile.objects.values('board').distinct()
    board_archive = Board.objects.filter(id__in=boards).order_by("-date_updated")

    activities = Board.objects.filter(menu__parent__id=33).order_by("-date_updated")
    main_img = Board.objects.filter(menu__parent__id=33).order_by("?")
    if main_img :
        try :
            main_img = main_img[0].get_files().order_by("?")[0].src.url
        except Exception:
            main_img = None

    latests = []
    board_recent = Board.objects.all().order_by("-date_updated")[:5]
    page_recent = Page.objects.all().order_by("-date_created")[:5]
    for ele in board_recent :
        latests.append({"unit":ele.menu.title,"title":ele.title,"url":"/board/detail/%d"%ele.id,"date":ele.date_updated})
    for ele in page_recent:
        if ele.menu.parent :
            latests.append({"unit": ele.menu.parent.title, "title": ele.menu.title,"url":"/menu/%d"%ele.menu.id,"date": ele.date_created})
        else :
            latests.append({"unit": ele.menu.title, "title": ele.menu.title, "url": "/menu/%d" % ele.menu.id,
                            "date": ele.date_created})

    latests = sorted(latests, key=itemgetter('date'), reverse=True)

    context = {
        'user':request.user,
        'lang':request.GET.get('lang'),
        'menu_icons':menu_icons,
        'menus': get_menu(),
        'main_img':main_img,
        'board_archive':board_archive,
        'latests':latests[:5],
        'activities':activities[:4],
        'meta': {'title': 'InC Lab', 'con': '정보·컴퓨팅교육 연구실 | Informatics & Computing Education Lab', 'image': '/static/img/ku.jpg'},
        'appname': 'main'
    }
    return render(request, 'main.html', context)

def account(request):
    username = request.POST.get('username')
    grade = int(request.POST.get('grade',0))
    msg = 0

    if username and grade :
        user = request.user
        if username != "" : user.first_name = username
        if grade : user.profile.grade = grade
        user.save()
        user.profile.save()
        msg = 200

    context = {
        'user': request.user,
        'lang': request.GET.get('lang'),
        'menus': get_menu(),
        'msg':msg,
        'meta': {'title': 'MyPage', 'con': '마이페이지입니다.','image': '/static/img/ku.jpg'},
        'appname': 'account'
    }
    return render(request, 'account.html', context)

def account_password(request):
    old_password = request.POST.get('old_password')
    new_password = request.POST.get('new_password')
    msg = 0

    if old_password and new_password :
        user = authenticate(username=request.user.username, password=old_password)
        if user :
            user.set_password(new_password)
            user.save()
            msg = 200
        else :
            msg = 403
        return HttpResponseRedirect('/auth/login/?from=/')

    context = {
        'user': request.user,
        'lang': request.GET.get('lang'),
        'menus': get_menu(),
        'msg':msg,
        'meta': {'title': '비밀번호변경', 'con': '비밀번호변경 페이지입니다.', 'image': '/static/img/ku.jpg'},
        'appname': 'account'
    }
    return render(request, 'account_password.html', context)

def auth_login(request):
    if request.user.id :
        return HttpResponseRedirect("/")
    email = request.POST.get("email")
    if email :
        password = request.POST.get("password")
        login_from = request.POST.get("from", '/')
        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            request.session.set_expiry(31536000)
            return HttpResponseRedirect(login_from)
        return HttpResponseRedirect("/auth/login/?from=%s&msg=403"%login_from)
    else :
        login_from = request.GET.get('from')
        msg = request.GET.get('msg')
        context = {
            'user': request.user,
            'lang': request.GET.get('lang'),
            'menus': get_menu(),
            'from':login_from,
            'msg':msg,
            'meta': {'title': '로그인', 'con': '로그인 페이지입니다.', 'image': '/static/img/ku.jpg'},
            'appname': 'login'
        }
        return render(request, 'login.html', context)

def auth_register(request):
    if request.user.id :
        return HttpResponseRedirect("/")
    email = request.POST.get("email")
    if email :
        password = request.POST.get("password")
        username = request.POST.get("username")
        grade = request.POST.get("grade")
        gender = request.POST.get("gender")

        try:
            user = User.objects.create_user(username=email, password=password, email=email, first_name=username)
            if user:
                profile = UserProfile.objects.create(user=user, grade=grade, gender=gender)
                user = authenticate(username=email, password=password)
                if user:
                    login(request, user)
                    request.session.set_expiry(31536000)
                    return HttpResponseRedirect('/')
        except Exception as e:
            pass
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else :
        context = {
            'user': request.user,
            'lang': request.GET.get('lang'),
            'menus': get_menu(),
            'meta': {'title': '회원가입', 'con': '회원가입 페이지입니다.', 'image': '/static/img/ku.jpg'},
            'appname': 'register'
        }
        return render(request, 'register.html', context)


def auth_register_school(request):
    come_from = request.GET.get("come_from")
    form_school = request.POST.get("school")

    if form_school :
        form_grade = request.POST.get("grade")
        form_year = request.POST.get("year")
        form_div = request.POST.get("div")
        userschool, created = UserSchool.objects.get_or_create(user=request.user)
        if userschool :
            userschool.grade = form_grade
            userschool.school = form_school
            userschool.year = form_year
            userschool.div = form_div
            userschool.save()
        return HttpResponseRedirect(come_from)

    if request.user.get_school() :
        if not come_from :
            return HttpResponseRedirect('/')
        return HttpResponseRedirect(come_from)

    grades = GRADE_IN_SCHOOL_CHOICES

    context = {
        'user': request.user,
        'lang': request.GET.get('lang'),
        'menus': get_menu(),
        'grades':grades,
        'come_from':come_from,
        'meta': {'title': '학교정보', 'con': '학교정보 페이지입니다.', 'image': '/static/img/ku.jpg'},
        'appname': 'register_school'
    }
    return render(request, 'register_school.html', context)

def auth_logout(request):
    login_from = request.POST.get("from", '/')
    logout(request)
    return HttpResponseRedirect(login_from)


def menu(request, menu_id=0):
    menu = get_or_none(Menu,id=int(menu_id))
    if menu.mode == 1 :
        return page(request, menu.id)
    elif menu.mode == 2 :
        return board(request, menu)
    elif menu.mode == 3:
        return board(request, menu)
    elif menu.mode == 5:
        return board_5(request, menu)
    elif menu.mode == 6:
        return board_6(request, menu)

def page(request, menu_id=0):
    lang = request.GET.get('lang')
    page = get_or_none(Page,menu__id=menu_id)

    if lang == 'en' : page.contents = page.contents_en
    elif lang == 'jp' : page.contents = page.contents_jp

    context = {
        'user': request.user,
        'lang': lang,
        'page':page,
        'menus': get_menu(),
        'meta': {'title': set_menu_title(page.menu,lang), 'con': '%s페이지입니다.'%set_menu_title(page.menu,lang), 'image': '/static/img/ku.jpg'},
        'appname': page.menu.appname
    }
    return render(request, 'page.html', context)


def page_edit(request, menu_id=0):
    if not request.user.is_active : return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    menu_id = int(menu_id)
    lang = request.GET.get('lang')
    page = get_or_none(Page,menu_id=menu_id)

    contents = request.POST.get('contents')
    if contents:
        if lang == 'en':
            page.contents_en = contents
        elif lang == 'jp':
            page.contents_jp = contents
        else:
            page.contents = contents

        page.user = request.user
        page.date_created = timezone.now()
        page.save()

        if lang == 'en':
            return HttpResponseRedirect('/menu/%d?lang=en' % menu_id)
        elif lang == 'jp':
            return HttpResponseRedirect('/menu/%d?lang=jp' % menu_id)
        return HttpResponseRedirect('/menu/%d' % menu_id)

    if lang == 'en':
        page.contents = page.contents_en
    elif lang == 'jp':
        page.contents = page.contents_jp

    context = {
        'user': request.user,
        'lang': lang,
        'page':page,
        'menus': get_menu(),
        'meta': {'title': "%s 수정"%set_menu_title(page.menu, lang), 'con': '%s페이지 수정입니다.' % set_menu_title(page.menu, lang),
                 'image': '/static/img/ku.jpg'},
        'appname': page.menu.appname
    }
    return render(request, 'page_edit.html', context)

@csrf_exempt
def page_upload(request):
    filename = ""
    CKEditorFuncNum = request.GET.get('CKEditorFuncNum')
    try :
        if 'upload' in request.FILES:
            file = request.FILES['upload']
            filename = "%s.jpg"%(str(time.time()))
            fp = open('%s/%s' % ('/home/inc/www/inc/inc/media/page/', filename) , 'wb')
            for chunk in file.chunks():
                fp.write(chunk)
            fp.close()
    except Exception as e :
        return HttpResponse('%s'%e)
    return HttpResponse("""
        <script type='text/javascript'>
        window.parent.CKEDITOR.tools.callFunction(%s, '%s','업로드를 성공하였습니다.');
        </script>
        """ % (CKEditorFuncNum, '/media/page/%s' % filename))


def paper(request):
    lang = request.GET.get('lang')
    menu = get_or_none(Menu,id=11)
    papers_0 = DocPaper.objects.filter(type=0).order_by("-date_publication")
    papers_1 = DocPaper.objects.filter(type=1).order_by("-date_publication")
    papers_2 = DocPaper.objects.filter(type=2).order_by("-date_publication")
    papers_3 = DocPaper.objects.filter(type=3).order_by("-date_publication")
    context = {
        'user': request.user,
        'lang': lang,
        'menu':menu,
        'menus': get_menu(),
        'meta': {'title': '논문', 'con': '논문리스트입니다.', 'image': '/static/img/ku.jpg'},
        'papers_0':papers_0,
        'papers_1': papers_1,
        'papers_2': papers_2,
        'papers_3': papers_3,
        'appname': 'paper'
    }
    return render(request, 'paper.html', context)

def paper_add(request):
    lang = request.GET.get('lang')
    menu = get_or_none(Menu, id=11)
    context = {
        'user': request.user,
        'lang': lang,
        'menu': menu,
        'types':TYPE_IN_PAPER_CHOICES,
        'menus': get_menu(),
        'meta': {'title': '논문추가', 'con': '논문추가 페이지입니다.', 'image': '/static/img/ku.jpg'},
        'appname': 'paper'
    }
    return render(request, 'paper_add.html', context)


def book(request):
    lang = request.GET.get('lang')
    menu = get_or_none(Menu,id=61)
    books = DocBook.objects.all().order_by("-date_publication")
    context = {
        'user': request.user,
        'lang': lang,
        'menu':menu,
        'menus': get_menu(),
        'meta': {'title': '저서', 'con': '저서리스트입니다.', 'image': '/static/img/ku.jpg'},
        'books':books,
        'appname': 'book'
    }
    return render(request, 'book.html', context)


def board(request, menu=None):
    lang = request.GET.get('lang')
    page = request.GET.get('page',1)
    if menu :
        list = Board.objects.filter(menu=menu).order_by("-date_updated")
        list = Paginator(list, 15)
        context = {
            'menu':menu,
            'list':list.page(page),
            'user': request.user,
            'lang': lang,
            'menus': get_menu(),
            'meta': {'title': "%s" % set_menu_title(menu, lang),
                     'con': '%s 게시판 입니다.' % set_menu_title(menu, lang),
                     'image': '/static/img/ku.jpg'},
            'appname':'board_%d'%(menu.mode)
        }
        return render(request, 'board_%d.html'%(menu.mode), context)
    return HttpResponseRedirect('/')

def board_5(request, menu=None):
    lang = request.GET.get('lang')
    page = request.GET.get('page',1)
    if menu :
        boards = BoardFile.objects.values('board').distinct()
        list = Board.objects.filter(id__in=boards).order_by("-date_updated")
        list = Paginator(list, 15)
        context = {
            'menu':menu,
            'list':list.page(page),
            'user': request.user,
            'lang': lang,
            'menus': get_menu(),
            'meta': {'title': "%s" % set_menu_title(menu, lang),
                     'con': '%s 게시판 입니다.' % set_menu_title(menu, lang),
                     'image': '/static/img/ku.jpg'},
            'appname':'board_%d'%(menu.mode)
        }
        return render(request, 'board_%d.html'%(menu.mode), context)
    return HttpResponseRedirect('/')

def board_6(request, menu=None):
    lang = request.GET.get('lang')
    page = request.GET.get('page',1)
    if menu :
        list = Board.objects.filter(menu=menu).order_by("-date_updated")
        list = Paginator(list, 15)
        context = {
            'menu':menu,
            'list':list.page(page),
            'user': request.user,
            'lang': lang,
            'menus': get_menu(),
            'meta': {'title': "%s" % set_menu_title(menu, lang),
                     'con': '%s 게시판 입니다.' % set_menu_title(menu, lang),
                     'image': '/static/img/ku.jpg'},
            'appname':'board_%d'%(menu.mode)
        }
        return render(request, 'board_%d.html'%(menu.mode), context)
    return HttpResponseRedirect('/')

def board_write(request, menu_id=None):
    if not request.user.is_superuser : return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    menu = get_or_none(Menu,id=menu_id)
    lang = request.GET.get('lang')
    if request.POST.get("input_title") :
        input_title = request.POST.get("input_title")
        input_con = request.POST.get("input_con")
        input_headline = int(request.POST.get("input_headline",0))
        board = Board.objects.create(menu=menu,user=request.user,title=input_title,con=input_con,is_headline=input_headline)
        if board :
            for img_file in request.FILES.getlist('input_file'):
                board_img = BoardFile.objects.create(board=board, src="", is_visible=True)
                board_img.src.save(img_file.name, ContentFile(img_file.read()))
            return HttpResponseRedirect("/board/detail/%d"%(board.id))
    if menu :
        context = {
            'menu':menu,
            'user': request.user,
            'lang': lang,
            'menus': get_menu(),
            'meta': {'title': "%s 글쓰기" % set_menu_title(menu, lang),
                     'con': '%s 게시판 글쓰기 입니다.' % set_menu_title(menu, lang),
                     'image': '/static/img/ku.jpg'},
            'appname':'board_write'
        }
        return render(request, 'board_write.html', context)
    return HttpResponseRedirect('/')

def board_detail(request, board_id=None):
    board = get_or_none(Board,id=board_id)
    lang = request.GET.get('lang')
    if board :
        board.hits = board.hits+1
        board.save()
        boardfile = BoardFile.objects.filter(board=board)
        contents = board.con
        for i in range(0,len(boardfile)) :
            contents = contents.replace("{{%d}}"%i, "<a href='%s' target='_blank'><img src='%s' class='img_board_src'></a>"%(boardfile[i].src.url,boardfile[i].src.url))
        meta = {'title':board.title,'con':board.get_con,'image':''}
        if boardfile :
            meta['image'] = boardfile[0].src.url
        else :
            meta['image'] = '/static/img/ku.jpg'
        context = {
            'menu':board.menu,
            'board':board,
            'contents':contents,
            'user': request.user,
            'lang': lang,
            'menus': get_menu(),
            'meta':meta,
            'appname':'board_detail'
        }
        return render(request, 'board_detail.html', context)
    return HttpResponseRedirect('/')

def board_modify(request, board_id=None):
    if not request.user.is_superuser: return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    board = get_or_none(Board,id=board_id)
    lang = request.GET.get('lang')
    if request.POST.get("input_title") :
        input_title = request.POST.get("input_title")
        input_con = request.POST.get("input_con")
        input_headline = int(request.POST.get("input_headline",0))
        board.title = input_title
        board.con = input_con
        board.is_headline = input_headline
        board.save()
        if board :
            for img_file in request.FILES.getlist('input_file'):
                board_img = BoardFile.objects.create(board=board, src="", is_visible=True)
                board_img.src.save(img_file.name, ContentFile(img_file.read()))
            return HttpResponseRedirect("/board/detail/%d"%(board.id))
    if board :
        contents = board.con
        boardfile = BoardFile.objects.filter(board=board)
        meta = {'title': board.title, 'con': board.get_con, 'image': ''}
        if boardfile:
            meta['image'] = boardfile[0].src.url
        else:
            meta['image'] = '/static/img/ku.jpg'
        context = {
            'board':board,
            'menu':board.menu,
            'contents':contents,
            'user': request.user,
            'lang': lang,
            'menus': get_menu(),
            'meta':meta,
            'appname':'board_write'
        }
        return render(request, 'board_write.html', context)
    return HttpResponseRedirect('/')

def board_delete(request):
    if not request.user.is_superuser: return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    menu_id = 0
    board_id = request.POST.get("board_id")
    board = get_or_none(Board,id=board_id)
    menu_id = board.menu.id
    board.delete()
    return HttpResponse("/menu/%d"%menu_id)

def board_reply(request, board_id=None):
    boardreply = BoardReply.objects.filter(board=board_id).order_by("-date_updated")
    context = {
        'boardreply':boardreply,
        'user': request.user
    }
    return render(request, 'board_reply.html', context)

def board_reply_post(request):
    board_id = request.POST.get("board_id")
    con = request.POST.get("con")
    BoardReply.objects.create(board_id=board_id,user=request.user,con=con)
    return board_reply(request, board_id)

def board_reply_delete(request):
    boardreply_id = request.POST.get("boardreply_id")
    boardreply = get_or_none(BoardReply,id=boardreply_id)
    if boardreply :
        if boardreply.user == request.user or request.user.is_superuser :
            board = boardreply.board
            boardreply.delete()
            return board_reply(request, board.id)
    return HttpResponse("로드 실패")


def test(request):
    # list = []
    # papers = DocPaper.objects.all()
    # for paper in papers :
    #     if paper.page.find('no.') != -1 :
    #         list.append(paper.id)
    #         paper.page = paper.page.replace('no.','No.')
    #         paper.save()
    return HttpResponse("OK")

def JudgeOnline(request):
    return HttpResponseRedirect("http://163.152.112.7:8080/JudgeOnline")

def get_menu():
    return Menu.objects.filter(is_active=True,parent=None).order_by('order')