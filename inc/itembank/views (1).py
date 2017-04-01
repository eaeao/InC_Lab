import json
from base64 import b64decode

from django.core.files.base import ContentFile
from django.db.models import Q, Count
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from inc.itembank.models import Unit1, Unit2, Unit3, Question, Content, ChoiceItem, ImageItem, Testpaper, \
    TestpaperQuestion, TestpaperQuestionChoiceItem, TestpaperResult, TestpaperQuestionResult
from inc.main.models import get_or_none, UserSchool


def itembank_question(request):
    user = request.user
    if not request.session.get('guest'):
        if request.user.id:
            if not request.user.get_school():
                return HttpResponseRedirect('/auth/register/school/?come_from=/itembank/')
        else:
            return HttpResponseRedirect('/auth/register/guest/?come_from=/itembank/')
    else:
        user = request.session.get('guest')

    questions = Question.objects.filter(~Q(unit=22)).order_by("-id")

    context = {
        'user': user,
        'meta': {'title': '문제은행', 'con': '문제은행입니다.', 'image': '/static/img/ku.jpg'},
        'questions': questions,
        'appname': 'itembank_question'
    }
    return render(request, 'itembank_question.html', context)


def itembank_question_mine(request):
    user = request.user
    if not request.session.get('guest'):
        if request.user.id:
            if not request.user.get_school():
                return HttpResponseRedirect('/auth/register/school/?come_from=/itembank/')
        else:
            return HttpResponseRedirect('/auth/register/guest/?come_from=/itembank/')
    else:
        user = request.session.get('guest')

    questions = Question.objects.filter(~Q(unit=22) & Q(user=request.user)).order_by("-id")

    context = {
        'user': user,
        'meta': {'title': '문제은행', 'con': '문제은행입니다.', 'image': '/static/img/ku.jpg'},
        'questions': questions,
        'appname': 'itembank_question_mine'
    }
    return render(request, 'itembank_question.html', context)


def itembank_question_other(request):
    user = request.user
    if not request.session.get('guest'):
        if request.user.id:
            if not request.user.get_school():
                return HttpResponseRedirect('/auth/register/school/?come_from=/itembank/')
        else:
            return HttpResponseRedirect('/auth/register/guest/?come_from=/itembank/')
    else:
        user = request.session.get('guest')

    questions = Question.objects.filter(~Q(unit=22) & ~Q(user=request.user)).order_by("-id")

    context = {
        'user': user,
        'lang': request.GET.get('lang'),
        'meta': {'title': '문제은행', 'con': '문제은행입니다.', 'image': '/static/img/ku.jpg'},
        'questions': questions,
        'appname': 'itembank_question_other'
    }
    return render(request, 'itembank_question.html', context)


def itembank_question_detail(request, qid=0):
    user = request.user
    if not request.session.get('guest'):
        if request.user.id:
            if not request.user.get_school():
                return HttpResponseRedirect('/auth/register/school/?come_from=/itembank/')
        else:
            return HttpResponseRedirect('/auth/register/guest/?come_from=/itembank/')
    else:
        user = request.session.get('guest')

    context = {
        'user': user,
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
            example_img = request.POST['example_img'].partition('base64,')[2]
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

            if example_img :
                image_data = b64decode(example_img)
                question.src.save('example_img.png', ContentFile(image_data), save=True)

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
        return HttpResponseRedirect('/itembank/question/')
    else:
        context = {
            'user': request.user,
            'meta': {'title': '문제 만들기', 'con': '문제 만들기입니다.', 'image': '/static/img/ku.jpg'},
            'appname': 'itembank_question_write'
        }
        return render(request, 'itembank_question_write.html', context)


def itembank_write_selects(request):

    unit1_id = int(request.POST.get("unit1",1))
    unit2_id = int(request.POST.get("unit2",0))
    unit3_id = int(request.POST.get("unit3",0))
    unit1, uni2, uni3 = None, None, None

    unit1 = Unit1.objects.filter(~Q(id=4))
    if unit3_id != 0 :
        ele_unit3 = get_or_none(Unit3, id=unit3_id)
        unit3 = Unit3.objects.filter(unit=ele_unit3.unit)
        unit2 = Unit2.objects.filter(unit=ele_unit3.unit.unit)
        unit3_id = ele_unit3.id
        unit2_id = ele_unit3.unit.id
        unit1_id = ele_unit3.unit.unit.id
    elif unit2_id != 0 :
        unit3 = Unit3.objects.filter(unit=unit2_id)
        unit2 = Unit2.objects.filter(unit=unit3[0].unit.unit)
        unit3_id = unit3[0].id
        unit2_id = unit2_id
        unit1_id = unit3[0].unit.unit.id
    elif unit1_id != 0 :
        unit2 = Unit2.objects.filter(unit=unit1_id)
        unit3 = Unit3.objects.filter(unit=unit2[0])
        unit3_id = unit3[0].id
        unit2_id = unit2[0].id
        unit1_id = unit1_id

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
    return HttpResponseRedirect('/itembank/question/')


def itembank_testpaper(request):
    user = request.user
    if not request.session.get('guest'):
        if request.user.id:
            if not request.user.get_school():
                return HttpResponseRedirect('/auth/register/school/?come_from=/itembank/')
        else:
            return HttpResponseRedirect('/auth/register/guest/?come_from=/itembank/')
    else :
        user = request.session.get('guest')

    testpapers = Testpaper.objects.all().order_by("-id")

    context = {
        'user': user,
        'meta': {'title': '문제은행', 'con': '문제은행입니다.', 'image': '/static/img/ku.jpg'},
        'testpapers':testpapers,
        'appname': 'itembank_testpaper'
    }
    return render(request, 'itembank_testpaper.html', context)

def itembank_testpaper_mine(request):
    user = request.user
    if not request.session.get('guest'):
        if request.user.id:
            if not request.user.get_school():
                return HttpResponseRedirect('/auth/register/school/?come_from=/itembank/')
        else:
            return HttpResponseRedirect('/auth/register/guest/?come_from=/itembank/')
    else:
        user = request.session.get('guest')

    testpapers = Testpaper.objects.filter(user=request.user).order_by("-id")

    context = {
        'user': user,
        'meta': {'title': '문제은행', 'con': '문제은행입니다.', 'image': '/static/img/ku.jpg'},
        'testpapers':testpapers,
        'appname': 'itembank_testpaper_mine'
    }
    return render(request, 'itembank_testpaper.html', context)

def itembank_testpaper_other(request):
    user = request.user
    if not request.session.get('guest'):
        if request.user.id:
            if not request.user.get_school():
                return HttpResponseRedirect('/auth/register/school/?come_from=/itembank/')
        else:
            return HttpResponseRedirect('/auth/register/guest/?come_from=/itembank/')
    else:
        user = request.session.get('guest')

    testpapers = Testpaper.objects.filter(~Q(user=request.user)).order_by("-id")

    context = {
        'user': user,
        'meta': {'title': '문제은행', 'con': '문제은행입니다.', 'image': '/static/img/ku.jpg'},
        'testpapers':testpapers,
        'appname': 'itembank_testpaper_other'
    }
    return render(request, 'itembank_testpaper.html', context)


def itembank_testpaper_write(request):
    user = request.user
    if not request.session.get('guest'):
        if request.user.id:
            if not request.user.get_school():
                return HttpResponseRedirect('/auth/register/school/?come_from=/itembank/')
        else:
            return HttpResponseRedirect('/auth/register/guest/?come_from=/itembank/')
    else:
        user = request.session.get('guest')

    testpaper_title = request.POST.get("testpaper_title")
    if testpaper_title :
        try :
            questions_id = request.POST.getlist("questions_id[]")
            testpaper, created = Testpaper.objects.get_or_create(user=request.user,title=testpaper_title)
            if testpaper:
                for question_id in questions_id:
                    question = get_or_none(Question,id=question_id)
                    if question :
                        testpaper_question = TestpaperQuestion.objects.create(testpaper=testpaper,question=question)
                        contents = question.get_contents()
                        for content in contents:
                            if content.type == "answer_choice":
                                items = content.get_items()
                                for item in items :
                                    tqcs, created_3 = TestpaperQuestionChoiceItem.objects.get_or_create(testpaper_question=testpaper_question,choice_item=item)
            return HttpResponse("0")
        except Exception as e:
            return HttpResponse("%s"%e)

    questions = Question.objects.filter(~Q(unit=22)).order_by("-id")

    context = {
        'user': user,
        'meta': {'title': '문제은행', 'con': '문제은행입니다.', 'image': '/static/img/ku.jpg'},
        'questions':questions,
        'appname': 'itembank_testpaper_write'
    }
    return render(request, 'itembank_testpaper_write.html', context)


def itembank_testpaper_detail(request, tpid=0):
    user = request.user
    if not request.session.get('guest'):
        if request.user.id:
            if not request.user.get_school():
                return HttpResponseRedirect('/auth/register/school/?come_from=/itembank/')
        else:
            return HttpResponseRedirect('/auth/register/guest/?come_from=/itembank/')
    else:
        user = request.session.get('guest')

    testpaper = get_or_none(Testpaper,id=tpid)

    json_data = request.POST.get("questions")

    if type(user) is dict:
        if json_data:
            json_data = json.loads(json_data)
            school = request.POST.get("school")
            year = request.POST.get("year", 0)
            div = request.POST.get("div")

            request.session['guest']['get_school']['school'] = school
            request.session['guest']['get_school']['year'] = year
            request.session['guest']['get_school']['div'] = div
            user = request.session.get('guest')

            tr, created = TestpaperResult.objects.get_or_create(first_name=user['first_name'],email=user['email'],grade=user['grade'],
                                                                gender=user['gender'],school_grade=user['get_school']['grade'],school=user['get_school']['school'],
                                                                year=user['get_school']['year'],div=user['get_school']['div'],testpaper=testpaper)
            if tr:
                for ele in json_data:
                    TestpaperQuestionResult.objects.get_or_create(testpaper_result=tr, testpaper_question=get_or_none(TestpaperQuestion, id=ele['tqid']), answer=ele['answer'])
        results = TestpaperResult.objects.filter(email=user['email'], testpaper=testpaper)
    elif user :
        if json_data:
            json_data = json.loads(json_data)
            school = request.POST.get("school")
            year = request.POST.get("year", 0)
            div = request.POST.get("div")

            user_school = get_or_none(UserSchool, user=user)
            user_school.school = school
            user_school.year = year
            user_school.div = div
            user_school.save()

            tr, created = TestpaperResult.objects.get_or_create(user=user, testpaper=testpaper, school=school, year=year, div=div)
            if tr:
                for ele in json_data:
                    TestpaperQuestionResult.objects.get_or_create(testpaper_result=tr, testpaper_question=get_or_none(TestpaperQuestion, id=ele['tqid']), answer=ele['answer'])
        results = TestpaperResult.objects.filter(user=user, testpaper=testpaper)

    context = {
        'user': user,
        'lang': request.GET.get('lang'),
        'meta': {'title': '시험지 #%s'%tpid, 'con': '문제은행입니다.', 'image': '/static/img/ku.jpg'},
        'testpaper':testpaper,
        'results':results,
        'json_data':json_data,
        'appname': 'itembank_testpaper_detail'
    }
    return render(request, 'itembank_testpaper_detail.html', context)


def itembank_testpaper_analysis(request, tpid=0, tprid=None):
    if request.user :
        if not request.user.is_superuser :
            return HttpResponseRedirect("/itembank/testpaper/")

    testpaper = get_or_none(Testpaper, id=tpid)
    results = TestpaperResult.objects.filter(testpaper=testpaper)

    if tprid :
        appname = 'itembank_testpaper_analysis_each'
        results = results[int(tprid)]
    else :
        appname = 'itembank_testpaper_analysis'
        results = sorted(results, key=lambda res: res.get_score(), reverse=True)
        tqs = TestpaperQuestion.objects.filter(testpaper=testpaper)
        results_analysis = []
        for tq in tqs :
            tqrs = TestpaperQuestionResult.objects.filter(testpaper_question=tq).values('answer').annotate(Count('answer'))
            tmp = {}
            for tqr in tqrs :
                tmp[tqr['answer']] = tqr['answer__count']
            results_analysis.append(tmp)

    context = {
        'user': request.user,
        'meta': {'title': '시험지 #%s'%tpid, 'con': '문제은행입니다.', 'image': '/static/img/ku.jpg'},
        'testpaper':testpaper,
        'results':results,
        'results_analysis':results_analysis,
        'appname': appname
    }
    return render(request, 'itembank_testpaper_analysis.html', context)