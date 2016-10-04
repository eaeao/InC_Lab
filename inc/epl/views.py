from django.shortcuts import render

# Create your views here.
from inc.epl.models import EPL
from inc.main.models import get_or_none, Menu


def epl(request, eplname=""):
    epl = get_or_none(EPL,appname=eplname)
    menu = get_or_none(Menu, title=eplname)
    context = {
        'user': request.user,
        'epl':epl,
        'menu':menu,
        'appname': 'epl'
    }
    return render(request, 'epl.html', context)
