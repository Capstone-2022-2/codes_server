from datetime import datetime

from django.http import HttpResponseRedirect, JsonResponse, request
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from upracticeapp.models import Upractice


def upractice_main(request):
    uall = Upractice.objects.filter(writer=request.user) # main에서 들어오는 Upractice의 모든 값을 uall에 저장
    context = {'uall': uall}
    return render(request, "upracticeapp/upractice_main.html", context)

def upractice_first(request):
    try:
        if request.method == "POST":
            utitle = request.POST.get('utitle')
            ucontent1 = request.POST.get('ucontent')
            ucontent = ucontent1.replace('\r', '')
            uresult = request.POST.get('uresult')
            print(utitle, ucontent, uresult, len(ucontent))

            upractice_data = Upractice()
            upractice_data.upractice_title = utitle
            upractice_data.upractice_content = ucontent
            upractice_data.upractice_result = uresult
            upractice_data.upractice_chnum = len(ucontent)
            upractice_data.writer = request.user
            upractice_data.save()
            print(upractice_data)

            uall = Upractice.objects.filter(writer=request.user)  # main에서 들어오는 Upractice의 모든 값을 uall에 저장
            context = {'uall': uall}
            url = "http://127.0.0.1:8000/upractice/"
            return HttpResponseRedirect(url, context)


    except Exception as identifier:
        print(identifier)

    return render(request, "upracticeapp/upractice_first.html")

def upractice_second(request, upractice_id):
        g = Upractice.objects.get(pk=upractice_id)
        context = {'g': g}
        print(g)
        return render(request, "upracticeapp/upractice_second.html", context)

@csrf_exempt
def delete_upractice(request):
    print('실행!')
    print(request.GET['upractice_id'])
    Upractice.objects.filter(pk=request.GET['upractice_id']).delete()
    return JsonResponse(data={})

def uresult(request):
    print("result 실행")

    if request.method == "GET":
        uuser = request.user
        uprac = Upractice()
        upday = datetime.now()
        uTIME = request.GET.get('TIME')
        uscore = request.GET.get('score')
        uspeed = (int(uscore) // int(uTIME)) * 60
        umiss = request.GET.get('miss')
        uscore2 = int(100 * ((int(uscore)-int(umiss))/int(uscore)))


        print(uTIME,uscore,umiss,uuser,uspeed)



        context = {'uTIME': uTIME, 'uscore': uscore, 'umiss':umiss, 'uuser':uuser, 'upday':upday,
                   'uspeed':uspeed, 'uscore2':uscore2,}
        return render(request, 'upracticeapp/upractice_uresult.html', context)


