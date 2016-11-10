from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from inc.erroranalysis.models import ErrorAnalysisResult
from inc.erroranalysis.views import get_input_cases, get_compile_result
from inc.evaluation.models import EvaluationQuestion, EvaluationRecord
from inc.main.models import get_or_none
from inc.main.views import get_menu
from static.js.evaluation.Lib.re import escape


def evaluation_question(request):
    if request.user.id :
        if not request.user.get_school():
            return HttpResponseRedirect('/auth/register/school/?come_from=/evaluation/')
    else :
        return HttpResponseRedirect('/auth/login/?come_from=/evaluation/')

    questions = EvaluationQuestion.objects.all().order_by("-id")

    context = {
        'user': request.user,
        'lang': request.GET.get('lang'),
        'questions': questions,
        'meta': {'title': '프로그래밍 평가', 'con': '프로그래밍 평가입니다.', 'image': '/static/img/ku.jpg'},
        'appname': 'evaluation_question'
    }
    return render(request, 'evaluation_question.html', context)

def evaluation_question_mine(request):
    if request.user.id :
        if not request.user.get_school():
            return HttpResponseRedirect('/auth/register/school/?come_from=/evaluation/')
    else :
        return HttpResponseRedirect('/auth/login/?come_from=/evaluation/')

    questions = EvaluationQuestion.objects.filter(user=request.user).order_by("-id")

    context = {
        'user': request.user,
        'lang': request.GET.get('lang'),
        'questions': questions,
        'meta': {'title': '프로그래밍 평가', 'con': '프로그래밍 평가입니다.', 'image': '/static/img/ku.jpg'},
        'appname': 'evaluation_question_mine'
    }
    return render(request, 'evaluation_question.html', context)

def evaluation_question_other(request):
    if request.user.id :
        if not request.user.get_school():
            return HttpResponseRedirect('/auth/register/school/?come_from=/evaluation/')
    else :
        return HttpResponseRedirect('/auth/login/?come_from=/evaluation/')

    questions = EvaluationQuestion.objects.filter(~Q(user=request.user)).order_by("-id")

    context = {
        'user': request.user,
        'lang': request.GET.get('lang'),
        'questions': questions,
        'meta': {'title': '프로그래밍 평가', 'con': '프로그래밍 평가입니다.', 'image': '/static/img/ku.jpg'},
        'appname': 'evaluation_question_other'
    }
    return render(request, 'evaluation_question.html', context)


def evaluation_question_detail(request, qid=None):
    question = get_or_none(EvaluationQuestion, id=qid)

    context = {
        'user': request.user,
        'lang': request.GET.get('lang'),
        'question': question,
        'meta': {'title': '프로그래밍 평가', 'con': '프로그래밍 평가입니다.', 'image': '/static/img/ku.jpg'},
        'appname': 'evaluation_question_detail'
    }
    return render(request, 'evaluation_question_detail.html', context)

def evaluation_question_detail_editor(request):
    question = get_or_none(EvaluationQuestion, id=request.POST.get("qid",None))
    context = {
        'user': request.user,
        'question': question,
    }
    return render(request, 'evaluation_question_detail_editor.html', context)


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


def evaluation_run(request):
    contents = request.POST.get('contents','')
    error_type = request.POST.get('error_type', '')
    result = request.POST.get('result', '')
    qid = request.POST.get('question')
    question = None
    if qid :
        question = get_or_none(EvaluationQuestion, id=int(qid))

    if request.user.id and question:
        last_result = ErrorAnalysisResult.objects.filter(user=request.user, question=question).order_by("-id")
        if last_result :
            if last_result[0].code != contents :
                if question :
                    ear, created = ErrorAnalysisResult.objects.get_or_create(user=request.user, question=question, code=contents, type=error_type, msg=result)
        else :
            ear, created = ErrorAnalysisResult.objects.get_or_create(user=request.user, question=question,
                                                                     code=contents, type=error_type, msg=result)

    return HttpResponse(escape(result))


def evaluation_table(request,page=1):
    page = int(page)

    ears = ErrorAnalysisResult.objects.filter(~Q(user__profile__grade=2)).order_by('id')
    ears = Paginator(ears, 300)
    ears = ears.page(page)

    context = {
        'user': request.user,
        'ears':ears,
    }
    return render(request, 'evaluation_table.html', context)