import json

from django.core.files.base import ContentFile
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from inc.itembank.models import Unit1, Unit2, Unit3, Question, Content, ChoiceItem, ImageItem
from inc.main.models import get_or_none


def itembank(request):

    questions = Question.objects.all().order_by("-id")
    my_questions = Question.objects.filter(user=request.user).order_by("-id")

    context = {
        'user': request.user,
        'questions':questions,
        'my_questions':my_questions,
        'appname': 'itembank'
    }
    return render(request, 'itembank.html', context)


def itembank_detail(request, qid=0):
    context = {
        'user': request.user,
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
                    arr_contents.append({'type': type, 'contents': ''})
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
            'appname': 'itembank_write'
        }
        return render(request, 'itembank_write.html', context)


def itembank_write_selects(request):

    unit1_id = int(request.POST.get("unit1",0))
    unit2_id = int(request.POST.get("unit2",0))
    unit3_id = int(request.POST.get("unit3",0))
    unit1, uni2, uni3 = None, None, None

    unit1 = Unit1.objects.all()
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