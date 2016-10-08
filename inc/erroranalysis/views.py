import contextlib
import random
import sys
from collections import Counter

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.utils.html import escape

from inc.erroranalysis.models import errorsanalysis_errors, ErrorAnalysisResult
from inc.evaluation.models import EvaluationQuestion
from inc.main.models import get_or_none
from inc.main.views import get_menu
from io import StringIO


def erroranalysis(request, qid=None):
    question = get_or_none(EvaluationQuestion,id=qid)

    context = {
        'user': request.user,
        'question':question,
        'lang': request.GET.get('lang'),
        'menus': get_menu(),
        'meta': {'title': '오류분석', 'con': '오류분석입니다.', 'image': '/static/img/ku.jpg'},
        'appname': 'erroranalysis'
    }
    return render(request, 'erroranalysis.html', context)


def erroranalysis_result(request):
    contents_ori = request.POST.get('contents','')
    qid = request.POST.get('question')
    question = None
    if qid :
        question = get_or_none(EvaluationQuestion, id=int(qid))
    error = None

    try :
        if question :
            contents = get_input_cases(str(contents_ori), question.get_cases().values_list('case', flat=True))
            if contents : result = get_compile_result(random.choice(contents))
            else : result = get_compile_result(str(contents_ori))
        else : result = get_compile_result(str(contents_ori))
        error = errorsanalysis_errors[-1]
    except Exception as e:
        exc_info = str(sys.exc_info()[0]).replace("<class '","").replace("'>","")
        for err in errorsanalysis_errors:
            if err['type'] == exc_info:
                result = err['msg']%(e)
                error = err
                break
            result = "%s"%(exc_info)

    if request.user.id and question:
        last_result = ErrorAnalysisResult.objects.filter(user=request.user, question=question).order_by("-id")
        if last_result :
            if last_result[0].code != contents_ori :
                if error and question :
                    ear, created = ErrorAnalysisResult.objects.get_or_create(user=request.user, question=question, code=contents_ori, type=error['type'], msg=result)
        else :
            ear, created = ErrorAnalysisResult.objects.get_or_create(user=request.user, question=question,
                                                                     code=contents_ori, type=error['type'], msg=result)

    return HttpResponse(escape(result))

def erroranalysis_analysis(request, qid=None):
    users_id = ErrorAnalysisResult.objects.filter(question_id=int(qid)).values('user').distinct()
    users = User.objects.filter(id__in=users_id)
    context = {
        'user': request.user,
        'users':users,
        'lang': request.GET.get('lang'),
        'menus': get_menu(),
        'qid':qid,
        'meta': {'title': '오류분석 결과분석', 'con': '오류분석 결과분석입니다.', 'image': '/static/img/ku.jpg'},
        'appname': 'erroranalysis_analysis'
    }
    return render(request, 'erroranalysis_analysis.html', context)


def erroranalysis_analysis_result(request):
    qid = int(request.POST.get('qid',0))
    uid = int(request.POST.get('uid', 0))
    error_user = get_or_none(User,id=uid)
    ears = ErrorAnalysisResult.objects.filter(user=error_user,question_id=qid)
    types = ears.values('type').values_list('type', flat=True)
    units = []

    errs = errorsanalysis_errors[:]

    for type in types :
        for i in range(0,len(errs)) :
            if errs[i]['type'] == type :
                units.append(errs[i].get("unit",""))
                break

    context = {
        'user': request.user,
        'error_user':error_user,
        'ears':ears,
        'types':dict(Counter(types)),
        'units':dict(Counter(units)),
    }
    return render(request, 'erroranalysis_analysis_result.html', context)


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


def get_input_cases(text, cases=[]):

    text = """
def get_auto_input(input_value):
    print("입력값:%s"%str(input_value))
    return input_value

"""+text

    input_cases = ["""input("입력값:")""","""input('입력값:')""","""input()"""]

    for input_case in input_cases:
        text = text.replace(input_case,'input()')

    test_case = []
    for case in cases :
        tmp = text[:]
        case_eles = case.split(';')
        for i in range(len(case_eles)):
            if case_eles[i] :
                tmp = tmp.replace("input()","get_auto_input(%s)"%str(case_eles[i]),i+1)
        test_case.append(tmp)
    return test_case


def get_compile_result(text):
    with stdoutIO() as s:
        exec(text)
    return s.getvalue()