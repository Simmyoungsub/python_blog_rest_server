from django.db import models

# Create your models here.

class User(models.Model):
    username=models.TextField(max_length=10)
    userpassword=models.TextField(max_length=30)

    #model을 json문자열로 변환
    #실제 화면으로 보낼때는 json문자열로 변환하여 데이터를 전달
    def as_json(self):
        return {
            'id' : self.id,
            'username' : self.username
        }

class Board(models.Model):
    title = models.TextField(max_length=30)
    content = models.TextField(max_length=255,null=True)

    def as_json(self):
        return {
            'seq' : self.id,
            'title' : self.title,
            'content' : self.content
        }
