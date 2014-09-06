# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Eventinfo(models.Model):
    event_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45, blank=True)
    location = models.CharField(max_length=45)
    datetime = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True)
    initiatedngo = models.CharField(max_length=45)
    createddatetime = models.DateTimeField(blank=True, null=True)
    updateddatetime = models.DateTimeField(blank=True, null=True)
    def __str__(self):              # __unicode__ on Python 2
        return self.name
    class Meta:
        managed = False
        db_table = 'eventinfo'

class UserNormal(models.Model):
    user_id = models.IntegerField(blank=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(auto_now_add=True)
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75,primary_key=True)
    points = models.IntegerField(default=0,blank=True)
    is_active = models.IntegerField(default=0,blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    session_id=models.CharField(max_length=45,null=True)
    def __str__(self):              # __unicode__ on Python 2
        return self.username
    class Meta:
        managed = False
        db_table = 'user_normal'
class ERD(models.Model):
    user_id = models.IntegerField(primary_key=True)
    event_id = models.IntegerField()
    registered_datetime = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)
    class Meta:
        managed = False
        db_table = 'event_registration_data'
class Ngo(models.Model):
    name = models.CharField(primary_key=True, max_length=45)
    text = models.TextField()
    class Meta:
        managed = False
        db_table = 'ngo'
class UCE(models.Model):
    user_id = models.IntegerField(primary_key=True)
    event_id = models.IntegerField()
    event_name= models.CharField(max_length=45)
    status = models.CharField(max_length=5)
    points = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'user_completed_events'
