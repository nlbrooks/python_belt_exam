from __future__ import unicode_literals
from django.db import models
from datetime import *
import bcrypt, re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager): 
    def create_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email is not valid"
        db_list = User.objects.filter(email=postData['email'])
        if len(db_list) > 0:
            errors['is_user'] = "Email is already taken"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters"
        if len(postData['confirm_password']) < 8:
            errors['confirm_password'] = (
                "Confirm password should be at least 8 characters")
        if postData['password'] != postData['confirm_password']:
            errors['pw_match'] = "Passwords should match"
        return errors
    
    def login_validator(self, postData):
        errors = {}
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email is not valid"
        else:
            db_list = User.objects.filter(email=postData['email'])
            if len(db_list) == 0:
                errors['not_user'] = "Email is not registered to an account"
            else:
                if not bcrypt.checkpw(postData['password'].encode(), 
                db_list[0].password.encode()):
                    errors['pw'] = "Password is incorrect"
        return errors

    def trip_validator(self, postData):
        errors = {}
        if len(postData['destination']) < 3:
            if len(postData['destination']) == 0:
                errors['destination'] = "Destination must be provided"
            else:
                errors['destination'] = "Destination should be at least 3 characters"
        if len(postData['plan']) < 3:
            if len(postData['plan']) == 0:
                errors['plan'] = "Plan must be provided"
            else:
                errors['plan'] = "Plan should be at least 3 characters"
        start = postData['start_date']
        end = postData['end_date']
        today = date.today()
        if str(start) < str(today):
            errors['start_date'] = "Time travel is not allowed. Select a future start date"
        if str(end) < str(start):
             errors['end_date'] = "Time travel is not allowed. Select an end date after start date"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.TextField()
    creator = models.ForeignKey(User, related_name="trips" )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Join(models.Model):
    user = models.ForeignKey(User, related_name="user_joins")
    trip = models.ForeignKey(Trip, related_name="trip_joins")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
