import json
from operator import itemgetter

from django.core.files.base import ContentFile
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from inc.itembank.models import Unit1, Unit2, Unit3, Question, Content, ChoiceItem, ImageItem, TestpaperRecord
from inc.main.models import get_or_none
from inc.main.views import get_menu

system_info = {"title":"문제은행"
    ,"menus":[
        {'appname':'itembank',"title":"시험지","url":""}
        ,{'appname':'itembank_item',"title":"문제","url":""}
    ]}


def itembank(request):
    if request.user.id:
        if not request.user.get_school() :
            return HttpResponseRedirect('/auth/register/school/?come_from=/itembank/')

    questions = Question.objects.filter(~Q(unit=22)).order_by("-id")
    my_questions = []
    if request.user.id : my_questions = Question.objects.filter(Q(user=request.user)&~Q(unit=22)).order_by("-id")

    context = {
        'user': request.user,
        'lang': request.GET.get('lang'),
        'info': system_info,
        'meta': {'title': '문제은행', 'con': '문제은행입니다.', 'image': '/static/img/ku.jpg'},
        'questions':questions,
        'my_questions':my_questions,
        'appname': 'itembank'
    }
    return render(request, 'itembank.html', context)


def itembank_detail(request, qid=0):
    context = {
        'user': request.user,
        'lang': request.GET.get('lang'),
        'info': system_info,
        'meta': {'title': '문제 #%s'%qid, 'con': '문제은행입니다.', 'image': '/static/img/ku.jpg'},
        'question':get_or_none(Question,id=qid),
        'appname': 'itembank_detail'
    }
    return render(request, 'itembank_detail.html', context)


def itembank_write(request):
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
            'appname': 'itembank_write'
        }
        return render(request, 'itembank_write.html', context)


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
    return render(request, 'itembank_write_selects.html', context)


def itembank_delete(request, qid=0):
    question = get_or_none(Question,id=qid)
    if question.user == request.user or request.user.is_superuser :
        question.delete()
    return HttpResponseRedirect('/itembank/')

def itembank_testpaper(request):

    if TestpaperRecord.objects.filter(user=request.user):
        return HttpResponse("<h1>이미 시험이 제출되었습니다.</h1>")

    contents = Content.objects.filter(type='answer_choice')

    questions = []
    for content in contents:
        questions.append(content.question)

    context = {
        'questions':questions,
        'user': request.user,
        'lang': request.GET.get('lang'),
        'info': system_info,
        'meta': {'title': '문제은행', 'con': '문제은행입니다.', 'image': '/static/img/ku.jpg'},
        'appname': 'itembank_testpaper'
    }
    return render(request, 'itembank_testpaper.html', context)


def itembank_testpaper_submit(request):
    json_data = json.loads(request.POST.get("questions"))
    if json_data :
        for ele in json_data:
            TestpaperRecord.objects.create(user=request.user,question=get_or_none(Question,id=ele['qid']),items=ele['items'],answer=ele['answer'])

    context = {
        'user': request.user,
        'lang': request.GET.get('lang'),
        'menus': get_menu(),
        'meta': {'title': '문제은행', 'con': '문제은행입니다.', 'image': '/static/img/ku.jpg'},
        'appname': 'itembank_testpaper_submit'
    }
    return render(request, 'itembank_testpaper_submit.html', context)


def itembank_testpaper_analysis(request):

    questions_id = TestpaperRecord.objects.all().values('question').distinct()
    questions = Question.objects.filter(id__in=questions_id)

    context = {
        'user': request.user,
        'questions':questions,
        'lang': request.GET.get('lang'),
        'info': system_info,
        'meta': {'title': '문제은행', 'con': '문제은행입니다.', 'image': '/static/img/ku.jpg'},
        'appname': 'itembank_testpaper_analysis'
    }
    return render(request, 'itembank_testpaper_analysis.html', context)


def itembank_testpaper_analysis_result(request):
    import itertools
    question = get_or_none(Question,id=request.POST.get('qid'))
    records = TestpaperRecord.objects.filter(question=question)

    question_ids = []
    choice = get_or_none(Content,type='answer_choice',question=question)
    for ele in choice.get_items():
        question_ids.append(ele.id)

    permutations_list = list(itertools.permutations(question_ids))
    permutations = []

    for per in permutations_list:
        str_perm = "%d;%d;%d;%d;%d;"%(per[0],per[1],per[2],per[3],per[4])
        perm_correct = len(TestpaperRecord.objects.filter(question=question,items=str_perm,answer=choice.contents))
        perm_all = len(TestpaperRecord.objects.filter(question=question, items=str_perm))
        percent = 0.0
        try :
            percent = perm_correct/perm_all*100.0
        except:
            pass
        permutations.append({"key":str_perm,"value":"%d / %d"%(perm_correct,perm_all), "percent":percent})

        permutations = sorted(permutations, key=itemgetter('percent','value'), reverse=True)

    context = {
        'user': request.user,
        'records':records,
        'choice':choice,
        'permutations':permutations,
        'lang': request.GET.get('lang'),
        'info': system_info,
        'meta': {'title': '문제은행', 'con': '문제은행입니다.', 'image': '/static/img/ku.jpg'},
        'appname': 'itembank_testpaper_analysis_result'
    }
    return render(request, 'itembank_testpaper_analysis_result.html', context)


def itembank_testpaper_add(request):
    context = {
        'user': request.user,
        'lang': request.GET.get('lang'),
        'info': system_info,
        'meta': {'title': '문제은행', 'con': '문제은행입니다.', 'image': '/static/img/ku.jpg'},
        'appname': 'itembank_testpaper'
    }
    return render(request, 'itembank_testpaper_add.html', context)