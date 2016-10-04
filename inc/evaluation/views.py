from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from inc.erroranalysis.views import erroranalysis, get_input_cases, get_compile_result
from inc.evaluation.models import EvaluationQuestion, EvaluationRecord
from inc.main.models import get_or_none
from inc.main.views import get_menu


def evaluation(request):
    if request.user.id :
        if not request.user.get_school():
            return HttpResponseRedirect('/auth/register/school/?come_from=/evaluation/')

    questions = EvaluationQuestion.objects.all().order_by("-id")
    my_questions = []
    if request.user.id: my_questions = EvaluationQuestion.objects.filter(user=request.user).order_by("-id")

    context = {
        'user': request.user,
        'lang': request.GET.get('lang'),
        'menus': get_menu(),
        'questions': questions,
        'my_questions': my_questions,
        'meta': {'title': '프로그래밍 평가', 'con': '프로그래밍 평가입니다.', 'image': '/static/img/ku.jpg'},
        'appname': 'evaluation'
    }
    return render(request, 'evaluation.html', context)


def evaluation_detail(request, qid=None):
    return erroranalysis(request, qid)


def evaluation_result(request, qid=None):
    question = get_or_none(EvaluationQuestion,id=int(qid))
    source = request.POST.get("contents")

    if source :
        record, created = EvaluationRecord.objects.get_or_create(user=request.user, question=question, source_exec=source)
    else :
        record = EvaluationRecord.objects.filter(user=request.user,question=question).order_by("-id")
        if record :
            record = record[0]

    record_results = []
    contents = get_input_cases(str(record.source_exec), question.get_cases().values_list('case', flat=True))
    if contents :
        for content in contents :
            try :
                record_results.append(get_compile_result(content))
            except :
                record_results.append("ERROR")
    else :
        record_results.append(get_compile_result(record.source_exec))

    context = {
        'user': request.user,
        'lang': request.GET.get('lang'),
        'menus': get_menu(),
        'record':record,
        'record_results':record_results,
        'meta': {'title': '프로그래밍 평가', 'con': '프로그래밍 평가입니다.', 'image': '/static/img/ku.jpg'},
        'appname': 'evaluation_result'
    }
    return render(request, 'evaluation_result.html', context)


def evaluation_write(request):

    context = {
        'user': request.user,
        'lang': request.GET.get('lang'),
        'menus': get_menu(),
        'meta': {'title': '프로그래밍 평가', 'con': '프로그래밍 평가입니다.', 'image': '/static/img/ku.jpg'},
        'appname': 'evaluation_write'
    }
    return render(request, 'evaluation_write.html', context)