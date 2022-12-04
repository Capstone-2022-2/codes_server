from datetime import datetime

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse, request
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from upracticeapp.models import Upractice, Upresult


def upractice_main(request):
    uall = Upractice.objects.filter(writer=request.user) # main에서 들어오는 Upractice의 모든 값을 uall에 저장
    reverse_ulist = uall[::-1]
    context = {'uall': uall, 'reverse_ulist':reverse_ulist}
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
            local_url = "http://127.0.0.1:8000/upractice/"
            url = "http://15.164.3.60/upractice/"
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
        user = request.user
        uprac = Upractice()
        upnum = request.GET.get('upnum')
        upday = datetime.now()
        uTIME = request.GET.get('TIME')
        uscore = request.GET.get('score')
        uspeed = (int(uscore) // int(uTIME)) * 60
        umiss = request.GET.get('miss')
        uback = request.GET.get('back')
        uscore2 = 100 * (int(uscore) - (int(umiss) * 0.7 + int(uback) * 0.3)) / int(uscore)
        uscore2 = round(uscore2, 2)
        if uscore2 < 0:
            uscore2 = 0
        else:
            uscore2 = uscore2


        print(uTIME, uscore, umiss, user, uspeed, upnum, uscore2)



        context = {'uTIME': uTIME, 'uscore': uscore, 'upnum':upnum, 'umiss':umiss, 'user':user, 'upday':upday,
                   'uspeed':uspeed, 'uscore2':uscore2,}
        return render(request, 'upracticeapp/upractice_uresult.html', context)

def manage_uresult(request):
    if request.method == "POST" and 'umanageresult' in request.POST:
        print("POST 성공")
        upresult_accuracy = request.POST.get('uscore2')
        upresult_speed = request.POST.get('uspeed')
        udata_time = request.POST.get('upday')
        upresult_time = request.POST.get('utime')
        upresult_false_num = request.POST.get('umiss')
        upresult_summary = request.POST.get('usummary')
        user_id = request.user
        upractice_id = int(request.POST.get('upnum'))

        url = request.POST.get('url')
        print(url)

        print(url, upresult_accuracy, upresult_speed, udata_time, upresult_time, upresult_false_num, upresult_summary, user_id,
              upractice_id)

        if request.POST['umanageresult'] == '결과 저장하기':
            print("결과 저장")
            upresult_data = Upresult()
            upresult_data.upresult_accuracy = upresult_accuracy
            upresult_data.upresult_speed = upresult_speed
            upresult_data.udate_time = udata_time
            upresult_data.upresult_time = upresult_time
            upresult_data.upresult_false_num = upresult_false_num
            upresult_data.upresult_summary = upresult_summary
            upresult_data.user_id = User.objects.get(pk=user_id.pk)
            upresult_data.upractice_id = Upractice.objects.get(upractice_id=upractice_id)
            upresult_data.save()
            print('결과 저장 완료')
            return HttpResponseRedirect(url)
        elif request.POST['manageresult'] == '목록으로':
            print("다시")
            return render(request, 'upracticeapp/upractice_main.html')
        else:
            print("에러")