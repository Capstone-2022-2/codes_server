from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from postapp.views import PostCreateView, PostDetailView, PostUpdateView, PostDeleteView, PostListView, delete_comment, \
    delete

app_name = 'postapp'

urlpatterns = [

    path('list/', PostListView.as_view(), name='list'),
    path('create/', PostCreateView.as_view(), name='create'),
    path('detail/<int:pk>', PostDetailView.as_view(), name='detail'),
    path('update/<int:pk>', PostUpdateView.as_view(), name='update'),
    path('detail/delete', delete, name='delete'),
    path('detail/delete_comment/', delete_comment, name='delete_comment'),

]
