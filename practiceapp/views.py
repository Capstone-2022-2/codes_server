import random
import json
from datetime import datetime
from urllib import parse

import requests
from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import resolve

import practiceapp.models
from practiceapp.models import Language, Practice, Presult
from profileapp.models import Profile


def practice_first(request):
    return render(request, "practiceapp/practice_first.html")

def practice_create(request):
    if request.method == "GET":
        lang = Language.objects.all()
        context = {'lang':lang}
        return render(request, "practiceapp/create_code.html", context)
    elif request.method == "POST":
        language_id = request.POST.get('language_id')
        content1 = request.POST.get('content')
        content = content1.replace('\r','')
        result = request.POST.get('result')
        source = request.POST.get('source')


        practice_data = Practice()
        practice_data.code_language = Language.objects.get(pk=language_id)
        practice_data.code_content = content
        practice_data.code_result = result
        practice_data.code_source = source
        practice_data.practice_chnum = len(content)
        practice_data.save()


        context = {'language_id': language_id, 'content': content, 'result': result, 'source': source}

        return render(request, "practiceapp/practice_first.html", context)
    return render(request, "practiceapp/practice_first.html")


def practice_second(request):
    if request.method == "GET":
        if 'python' in request.GET:
            l = Language.objects.filter(language='python')
            i = Language.objects.get(pk=1)
            practice_lang = Practice.objects.filter(code_language=i)
            practice_list = list(practice_lang)
            random_practice = random.choice(practice_list)
            practice_select = Practice.objects.filter(pk=random_practice.practice_id)
            print(practice_select)
            # practice = serializers.serialize('json', practice_select)
            # print(practice)
            # print(type(practice))
            # practice_data = Practice.objects.values()
            # practice_data = list(practice_data)
            # practice_data = practice_data[0]
            # print(practice_data)
            # print(type(practice_data))
            # jpractice_data = json.dumps(practice_data)
            # print(jpractice_data)
            # print(type(jpractice_data))

            context = {'l':l, 'practice_select':practice_select}
            return render(request, 'practiceapp/practice_second.html', context)


        elif 'css' in request.GET:
            l = Language.objects.filter(language='css')
            i = Language.objects.get(pk=2)
            practice_lang = Practice.objects.filter(code_language=i)
            practice_list = list(practice_lang)
            random_practice = random.choice(practice_list)
            practice_select = Practice.objects.filter(pk=random_practice.practice_id)
            print(practice_select)

            context = {'l': l, 'practice_select': practice_select}
            return render(request, 'practiceapp/practice_second.html', context)


        elif 'html' in request.GET:
            l = Language.objects.filter(language='html')
            i = Language.objects.get(pk=3)
            practice_lang = Practice.objects.filter(code_language=i)
            practice_list = list(practice_lang)
            random_practice = random.choice(practice_list)
            practice_select = Practice.objects.filter(pk=random_practice.practice_id)
            print(practice_select)
            context = {'l': l, 'practice_select': practice_select}
            return render(request, 'practiceapp/practice_second.html', context)


        elif 'javascript' in request.GET:
            l = Language.objects.filter(language='javascript')
            i = Language.objects.get(pk=4)
            practice_lang = Practice.objects.filter(code_language=i)
            practice_list = list(practice_lang)
            random_practice = random.choice(practice_list)
            practice_select = Practice.objects.filter(pk=random_practice.practice_id)
            print(practice_select)
            context = {'l': l, 'practice_select': practice_select}
            return render(request, 'practiceapp/practice_second.html', context)

        return render(request, 'practiceapp/practice_second.html')



def result(request):
    print("result 실행")

    if request.method == "GET":
        user = request.user
        prac = Practice()
        pday = datetime.now()
        pnum = request.GET.get('pnum')
        TIME = request.GET.get('TIME')
        score = request.GET.get('score')
        speed = (int(score) // int(TIME)) * 60
        miss = request.GET.get('miss')
        back = request.GET.get('back')
        score2 = 100 * (int(score)-(int(miss)*0.7 + int(back)*0.3))/int(score)
        score2 = round(score2,2)

        if score2 < 0:
            score2 = 0
        else:
            score2 = score2

        print(pnum,TIME,score,miss,user,speed,score2)

        context = {'TIME': TIME, 'score': score, 'miss':miss, 'user':user, 'pday':pday,
                   'speed':speed, 'score2':score2, 'pnum':pnum}
        return render(request, 'practiceapp/practice_result.html', context)




def manage_result(request):
    if request.method == "POST" and 'manageresult' in request.POST:
        print("POST 성공")
        presult_accuracy = request.POST.get('score2')
        presult_speed = request.POST.get('speed')
        data_time = request.POST.get('pday')
        presult_time = request.POST.get('time')
        presult_false_num = request.POST.get('miss')
        presult_summary = request.POST.get('summary')
        user_id = request.user
        practice_id = int(request.POST.get('pnum'))
        # 현재주소받아와서리다이렉트에사용
        url = request.POST.get('url')
        print(url)
        print(presult_accuracy,presult_speed,data_time,presult_time,presult_false_num,presult_summary,user_id,practice_id)
        if request.POST['manageresult'] == '결과 저장하기':
            print("결과 저장")
            presult_data = Presult()
            presult_data.presult_accuracy = presult_accuracy
            presult_data.presult_speed = presult_speed
            presult_data.date_time = data_time
            presult_data.presult_time = presult_time
            presult_data.presult_false_num = presult_false_num
            presult_data.presult_summary = presult_summary
            presult_data.user_id = User.objects.get(pk=user_id.pk)
            presult_data.practice_id = Practice.objects.get(practice_id=practice_id)
            presult_data.save()
            print('결과 저장 완료')
            return HttpResponseRedirect(url)
        elif request.POST['manageresult'] == '다시하기':
            practice_id = Practice.objects.get(practice_id=practice_id)
            print("다시")
            return render(request, 'practiceapp/manage_result.html')
        else:
            print("다른 경우")
            return render(request, 'practiceapp/manage_result.html')
    elif request.method == "GET" and 'replay' in request.GET:
        if request.GET['replay'] == '계속하기':
            print('계속하기 선택')
            return render(request, 'practiceapp/practice_first.html')
        else:
            print("에러")
    else:
        print("모든 거 해당 X")


def rerere(request, pk):
    if request.method == "GET" and 'rerere' in request.GET:
        if request.GET['rerere'] == '다시하기':
            print('다시하기 선택')
            # pk = request.GET['pnum']
            print("re에서 pnum",pk)
            practice_select = Practice.objects.filter(pk=pk)
            print(practice_select)
            context = {'practice_select': practice_select}
            return render(request, 'practiceapp/practice_second.html', context)
        else:
            print("에러")
    return render(request, 'practiceapp/practice_second.html')