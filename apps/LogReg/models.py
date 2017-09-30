from __future__ import unicode_literals
from django.db import models
from re import match, search
from bcrypt import hashpw, gensalt

class UserManager(models.Manager):
    def register(self, name, username, password, conf_password, csrfmiddlewaretoken):
        messagelist = []
        
        name = name[0]
        if len(name) < 3:
            messagelist.append("Name must be at least 3 characters long")
        elif search(r'[^a-zA-Z\s]', name):
            messagelist.append("Name must only contain letters and spaces")
        
        username = username[0]
        if len(username) < 3:
            messagelist.append("Username must be at least 3 characters long")
        if not match(r'^[a-zA-Z0-9]+$', username):
            messagelist.append("Invalid Username")
        elif User.objects.filter(username=username):
            messagelist.append("Username already in use")
        
        password = password[0]
        if len(password) < 8:
            messagelist.append("Password must be at least 8 characters long")
        
        conf_password = conf_password[0]
        if conf_password != password:
            messagelist.append("Password does not match")
        
        if len(messagelist) == 0:
            pw_hash = hashpw(password.encode(), gensalt())
            new_user = User.objects.create(name=name, username=username, password=pw_hash)
            return (True, new_user.id)
        else:
            return (False, messagelist)
    def login(self, username, password):
        if User.objects.filter(username=username):
            user = User.objects.get(username=username)
            if hashpw(password.encode(), user.password.encode()) == user.password:
                return (True, user.id)
            else:
                return (False, "Invalid password")
        else:
            return (False, "Invalid username")

class User(models.Model):
    name = models.CharField(max_length=45)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    userManager = UserManager()
    objects = models.Manager()