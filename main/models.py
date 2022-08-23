from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    username=models.ForeignKey(User,on_delete=models.CASCADE)
    profile_pic=models.ImageField(default="npp.svg",upload_to="media",blank=True)
    cover_pic=models.ImageField(default="cover.png",upload_to="media",blank=True)
    bio=models.TextField(max_length=150)
    location=models.CharField(max_length=30)

    def __str__(self):
        return f'{self.username}'

class Post(models.Model):
    creator=models.ForeignKey(User,on_delete=models.CASCADE,related_name='creator')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    image=models.ImageField(upload_to="post",blank=True,null=True)
    text=models.TextField(max_length=200)
    likers=models.ManyToManyField(User,blank=True,related_name='likers')
    savers=models.ManyToManyField(User,blank=True,related_name='savers')

    def __str__(self):
        return f'{self.creator} + {self.text} +{self.created} + {self.updated}'
    
class Comment(models.Model):
    commenter=models.ForeignKey(User,on_delete=models.CASCADE,name="commenter")
    posts=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post')
    content=models.TextField(max_length=200)
    created=models.DateTimeField(auto_now=True)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)
    
    def __str__(self):
        return f'{self.commenter} +{self.posts}'
    
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-created').all()



class Followers(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    follower=models.ManyToManyField(User,related_name='follower')
    following=models.ManyToManyField(User,related_name='following')

    def __str__(self):
        return f'{self.user}'

# class ThreadModel(models.Model):
#     user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='+')
#     receiver=models.ForeignKey(User,on_delete=models.CASCADE,related_name='+')
    
# class MessageModel(models.Model):
#     thread=models.ForeignKey(ThreadModel,on_delete=models.CASCADE,related_name='+',blank=True,null=True)
#     sender_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='+')
#     receiver_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='+')
#     body=models.CharField(max_length=1000)
#     date=models.DateTimeField(auto_now_add=True)
#     is_read=models.BooleanField(default=False)
    
