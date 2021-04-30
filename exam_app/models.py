from django.db import models
import re# the regex module
import bcrypt

class Usermanager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['fname']) < 2:
            errors["fname"] = "first name should be at least 2 characters"
        if len(postData['lname']) < 2:
            errors["lname"] = "last name should be at least 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['pw']) < 8:
            errors["pw"] = "password should be at least 8 characters"
        if postData['confirm_pw'] != postData['pw']:
            errors["confirm_pw"] = "confirm password does not match with password"
        return errors

    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['pw']) < 8:
            errors["pw"] = "password should be at least 8 characters"

        return errors

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    Email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=Usermanager()


class WishManager(models.Manager):
    def wish_validator(self, post_data):
        errors = {}
        if len(post_data['item']) < 3:
            errors['item'] = "Your wish must be at least 3 characters"
        if len(post_data['desc']) < 3:
            errors['desc'] = "Description must be at least 3 characters"    
        return errors

class Wish (models.Model):
    item=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    granted=models.CharField(max_length=255)
    wisher=models.ForeignKey(User,related_name='wishes',on_delete=models.CASCADE)
    liked_by=models.ManyToManyField(User,related_name='liked_wishes')
    granted_for=models.ManyToManyField(User,related_name='granted_wish')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=WishManager()