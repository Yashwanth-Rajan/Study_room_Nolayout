from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission

# class User(AbstractUser):
#     name = models.CharField(max_length=200, null=True)
#     email = models.EmailField(unique=True, null=True)
#     bio = models.TextField(null=True)

#     avatar = models.ImageField(null=True, default="avatar.svg")

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):     #This used to view the name in the admin panel
        return self.name

#Relation - topic can have multiple rooms ,but a room can have only one topic.



class Room(models.Model):
    host = models.ForeignKey(User,on_delete = models.SET_NULL,null=True)
    topic = models.ForeignKey(Topic,on_delete = models.SET_NULL,null=True)
    name= models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)
    participants = models.ManyToManyField(User,related_name='participants',blank=True)


    class Meta:
        ordering = ['-updated','-created']
    
    def __str__(self):     #This used to view the name in the admin panel
        return self.name
    

class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete = models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.body[0:50]
    
    class Meta:
        ordering = ['-updated','-created']