from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Upractice(models.Model):
    upractice_id = models.AutoField(primary_key=True)
    upractice_title = models.CharField(max_length=32, null=False)
    upractice_content = models.TextField(null=False)
    upractice_result = models.TextField(null=False)
    upractice_chnum = models.IntegerField(null=False)
    writer = models.ForeignKey(User,on_delete=models.CASCADE, null=False)

    def __str__(self):
        return str(self.upractice_id) + ' - ' + str(self.upractice_title) + ' - ' + str(self.upractice_chnum) + ' - ' + str(self.writer)

class Upresult(models.Model):
    upresult_id = models.AutoField(primary_key=True)
    upresult_accuracy = models.DecimalField(max_digits=5, decimal_places=2)
    upresult_speed = models.IntegerField(null=False)
    udate_time = models.DateTimeField(auto_now_add=True)
    upresult_time = models.IntegerField(null=False)
    upresult_false_num = models.IntegerField(null=False)
    upresult_summary = models.TextField(null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    upractice_id = models.ForeignKey(Upractice, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return str(self.upresult_id) + ' - ' + str(self.user_id)