from django.forms import ModelForm

from postapp.models import Post


class PostCreationForm(ModelForm):
    class Meta:
        model = Post
        fields = ['post_title', 'image', 'post_content']
        labels = {
            'post_title': '제목',
            'image': '이미지',
            'post_content': '내용'
        }
