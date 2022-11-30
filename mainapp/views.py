from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.views.generic.list import MultipleObjectMixin

from commentapp.models import Comment
from mainapp.forms import AccountUpdateForm
from postapp.models import Post
from upracticeapp.models import Upractice
from practiceapp.models import Presult
import pandas as pd


def main_page(request):
    return render(request, 'mainapp/mainpage.html')

class AccountCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('mainapp:mainpage')
    template_name = 'mainapp/signup.html'

class AccountDetailView(DetailView, MultipleObjectMixin):
    model = User
    context_object_name = 'target_user'
    template_name = 'mainapp/detail.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        object_list = Post.objects.filter(writer=self.get_object())
        object_list = object_list[::-1]
        return super(AccountDetailView, self).get_context_data(object_list=object_list, **kwargs)


class AccountUpdateView(UpdateView):
    model = User
    context_object_name = 'target_user'
    form_class = AccountUpdateForm
    success_url = reverse_lazy('mainapp:mainpage')
    template_name = 'mainapp/update.html'

class AccountDeleteView(DeleteView):
    model = User
    context_object_name = 'target_user'
    success_url = reverse_lazy('mainapp:login')
    template_name = 'mainapp/delete.html'


def practice_result(request, pk):
    print(pk)
    print(type(pk))
    user = User.objects.get(pk=pk)
    result_list = Presult.objects.filter(user_id=user.pk)

    # 소요시간, 타자속도, 오타횟수, 정확도, 날짜 리스트 생성
    new_list=[]
    re_time =[]
    re_speed =[]
    re_false_num =[]
    re_accuracy =[]
    re_date_time =[]

    # 쿼리셋형태를 단순 리스트로
    for i in result_list:
        new_list.append(i)

    # 리스트 안에 <>를 리스트로 변경
    new_list2=[]
    for j in range(len(new_list)):
        test = new_list[j]
        test = str(test)
        test2 = test.split(',')
        test2 = list(test2)
        new_list2.append(test2)

    for p in range(len(new_list)):
        re_time.append(new_list2[p][0])
        re_speed.append(new_list2[p][1])
        re_false_num.append(new_list2[p][2])
        re_accuracy.append(new_list2[p][3])
        re_date_time.append(new_list2[p][4])


    context = {'user': user, 'result_list': result_list, 're_time':re_time, 're_speed':re_speed, 're_false_num':re_false_num,
               're_accuracy':re_accuracy, 're_date_time':re_date_time}
    return render(request, 'mainapp/user_result.html', context)

def page_not_found(request, exception):
    """
    404 Page not found
    """
    print(exception)
    return render(request, 'error/404.html', {})