from django.core.files.base import ContentFile
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from inc.itembank.models import Unit1, Unit2, Unit3, Question, Content, ChoiceItem, ImageItem, Testpaper, \
    TestpaperQuestion, TestpaperQuestionChoiceItem
from inc.main.models import get_or_none

system_info = {"title":"문제은행"
    ,"menus":[
        {'appname':'itembank',"title":"시험지","url":""}
        ,{'appname':'itembank_item',"title":"문제","url":""}
    ]}


def itembank_question(request):
    if request.user.id:
        if not request.user.get_school() :
            return HttpResponseRedirect('/auth/register/school/?come_from=/itembank/')
    else :
        return HttpResponseRedirect('/auth/login/?come_from=/itembank/')

    questions = Question.objects.filter(~Q(unit=22)).order_by("-id")

    context = {
        'user': request.user,
        'lang': request.GET.get('lang'),
        'info': system_info,
        'meta': {'title': '문제은행', 'con': '문제은행입니다.', 'image': '/static/img/ku.jpg'},
        'questions':questions,
        'appname': 'itembank_question'
    }
    return render(request, 'itembank_question.html', context)

def itembank_question_mine(request):
    if request.user.id:
        if not request.user.get_school() :
            return HttpResponseRedirect('/auth/register/school/?come_from=/itembank/')
    else :
        return HttpResponseRedirect('/auth/login/?come_from=/itembank/')

    questions = Question.objects.filter(~Q(unit=22)&Q(user=request.user)).order_by("-id")

    context = {
        'user': request.user,
        'lang': request.GET.get('lang'),
        'info': system_info,
        'meta': {'title': '문제은행', 'con': '문제은행입니다.', 'image': '/static/img/ku.jpg'},
        'questions':questions,
        'appname': 'itembank_question_mine'
    }
    return render(request, 'itembank_question.html', context)

def itembank_question_other(request):
    if request.user.id:
        if not request.user.get_school() :
            return HttpResponseRedirect('/auth/register/school/?come_from=/itembank/')
    else :
        return HttpResponseRedirect('/auth/login/?come_from=/itembank/')

    questions = Question.objects.filter(~Q(unit=22)&~Q(user=request.user)).order_by("-id")

    context = {
        'user': request.user,
        'lang': request.GET.get('lang'),
        'info': system_info,
        'meta': {'title': '문제은행', 'con': '문제은행입니다.', 'image': '/static/img/ku.jpg'},
        'questions':questions,
        'appname': 'itembank_question_other'
    }
    return render(request, 'itembank_question.html', context)

def itembank_question_detail(request, qid=0):
    context = {
        'user': request.user,
        'lang': request.GET.get('lang'),
        'info': system_info,
        'meta': {'title': '문제 #%s'%qid, 'con': '문제은행입니다.', 'image': '/static/img/ku.jpg'},
        'question':get_or_none(Question,id=qid),
        'appname': 'itembank_question_detail'
    }
    return render(request, 'itembank_question_detail.html', context)


def itembank_question_write(request):
    title = request.POST.get('title')
    if title :
        try:
            unit3 = request.POST.get('unit3',0)
            images = request.FILES.getlist("image")
            arr_post = {}
            for post in request.POST:
                arr_post[post] = request.POST.getlist(post)

            arr_contents = []
            arr_choice_items = []
            for type in arr_post['type']:
                if type == "image" :
                    arr_contents.append({'type': type, 'contents': 'image'})
                elif type == "answer_choice" :
                    arr_contents.append({'type': type, 'contents': arr_post['answer_choice_radio'][0]})
                    arr_choice_items = arr_post['answer_choice'][:]
                    arr_post[type].pop(0)
                else :
                    arr_contents.append({'type':type,'contents':arr_post[type][0]})
                    arr_post[type].pop(0)

            question = Question.objects.create(unit=get_or_none(Unit3,id=unit3),user=request.user,title=title)
            for con in arr_contents:
                content = Content.objects.create(question=question,type=con['type'],contents=con['contents'])
                if content.type == "answer_choice" :
                    for item in arr_choice_items:
                        ChoiceItem.objects.create(content=content,text=item)
                elif content.type == "image" :
                    imageitem = ImageItem.objects.create(content=content,src="")
                    imageitem.src.save("%s.jpg" % images[0].name, ContentFile(images[0].read()))
                    images.pop(0)
        except Exception as e:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return HttpResponseRedirect('/itembank/')
    else:
        context = {
            'user': request.user,
            'lang': request.GET.get('lang'),
            'info': system_info,
            'meta': {'title': '문제 만들기', 'con': '문제 만들기입니다.', 'image': '/static/img/ku.jpg'},
            'appname': 'itembank_question_write'
        }
        return render(request, 'itembank_question_write.html', context)


def itembank_write_selects(request):

    unit1_id = int(request.POST.get("unit1",0))
    unit2_id = int(request.POST.get("unit2",0))
    unit3_id = int(request.POST.get("unit3",0))
    unit1, uni2, uni3 = None, None, None

    unit1 = Unit1.objects.filter(~Q(id=4))
    if unit1_id == 0 :
        if unit1[0] :
            unit1_id = unit1[0].id

    unit2 = Unit2.objects.filter(unit=unit1_id)
    if unit2_id == 0:
        if unit2[0] :
            unit2_id = unit2[0].id

    unit3 = Unit3.objects.filter(unit=unit2_id)

    context = {
        'user': request.user,
        'lang': request.GET.get('lang'),
        'unit1_id': unit1_id,
        'unit2_id': unit2_id,
        'unit3_id': unit3_id,
        'unit1': unit1,
        'unit2': unit2,
        'unit3': unit3,
        'appname': 'itembank_write_selects'
    }
    return render(request, 'itembank_question_write_selects.html', context)


def itembank_delete(request, qid=0):
    question = get_or_none(Question,id=qid)
    if question.user == request.user or request.user.is_superuser :
        question.delete()
    return HttpResponseRedirect('/itembank/')


def itembank_testpaper(request):
    if request.user.id:
        if not request.user.get_school() :
            return HttpResponseRedirect('/auth/register/school/?come_from=/itembank/')
    else :
        return HttpResponseRedirect('/auth/login/?come_from=/itembank/')

    testpapers = Testpaper.objects.all().order_by("-id")

    context = {
        'user': request.user,
        'lang': request.GET.get('lang'),
        'info': system_info,
        'meta': {'title': '문제은행', 'con': '문제은행입니다.', 'image': '/static/img/ku.jpg'},
        'testpapers':testpapers,
        'appname': 'itembank_testpaper'
    }
    return render(request, 'itembank_testpaper.html', context)

def itembank_testpaper_mine(request):
    if request.user.id:
        if not request.user.get_school() :
            return HttpResponseRedirect('/auth/register/school/?come_from=/itembank/')
    else :
        return HttpResponseRedirect('/auth/login/?come_from=/itembank/')

    testpapers = Testpaper.objects.filter(user=request.user).order_by("-id")

    context = {
        'user': request.user,
        'lang': request.GET.get('lang'),
        'info': system_info,
        'meta': {'title': '문제은행', 'con': '문제은행입니다.', 'image': '/static/img/ku.jpg'},
        'testpapers':testpapers,
        'appname': 'itembank_testpaper_mine'
    }
    return render(request, 'itembank_testpaper.html', context)

def itembank_testpaper_other(request):
    if request.user.id:
        if not request.user.get_school() :
            return HttpResponseRedirect('/auth/register/school/?come_from=/itembank/')
    else :
        return HttpResponseRedirect('/auth/login/?come_from=/itembank/')

    testpapers = Testpaper.objects.filter(~Q(user=request.user)).order_by("-id")

    context = {
        'user': request.user,
        'lang': request.GET.get('lang'),
        'info': system_info,
        'meta': {'title': '문제은행', 'con': '문제은행입니다.', 'image': '/static/img/ku.jpg'},
        'testpapers':testpapers,
        'appname': 'itembank_testpaper_other'
    }
    return render(request, 'itembank_testpaper.html', context)


def itembank_testpaper_write(request):
    if request.user.id:
        if not request.user.get_school() :
            return HttpResponseRedirect('/auth/register/school/?come_from=/itembank/')
    else :
        return HttpResponseRedirect('/auth/login/?come_from=/itembank/')

    testpaper_title = request.POST.get("testpaper_title")
    if testpaper_title :
        try :
            questions_id = request.POST.getlist("questions_id[]")
            testpaper, created = Testpaper.objects.get_or_create(user=request.user,title=testpaper_title)
            if testpaper:
                for question_id in questions_id:
                    question = get_or_none(Question,id=question_id)
                    if question :
                        testpaper_question, created_2 = TestpaperQuestion.objects.get_or_create(testpaper=testpaper,question=question)
                        contents = question.get_contents()
                        for content in contents:
                            if content.type == "answer_choice":
                                items = content.get_items_random()
                                for item in items :
                                    tqcs, created_3 = TestpaperQuestionChoiceItem.objects.get_or_create(testpaper_question=testpaper_question,choice_item=item)
            return HttpResponse("0")
        except Exception as e:
            return HttpResponse("%s"%e.with_traceback())

    questions = Question.objects.filter(~Q(unit=22)).order_by("-id")

    context = {
        'user': request.user,
        'lang': request.GET.get('lang'),
        'info': system_info,
        'meta': {'title': '문제은행', 'con': '문제은행입니다.', 'image': '/static/img/ku.jpg'},
        'questions':questions,
        'appname': 'itembank_testpaper_write'
    }
    return render(request, 'itembank_testpaper_write.html', context)


def itembank_testpaper_detail(request, tpid=0):
    context = {
        'user': request.user,
        'lang': request.GET.get('lang'),
        'info': system_info,
        'meta': {'title': '시험지 #%s'%tpid, 'con': '문제은행입니다.', 'image': '/static/img/ku.jpg'},
        'testpaper':get_or_none(Testpaper,id=tpid),
        'appname': 'itembank_testpaper_detail'
    }
    return render(request, 'itembank_testpaper_detail.html', context)