# -*- coding: cp1252 -*-
import django
import logging
from django.core.cache import cache
from theayudar.models import UserNormal,UserEvents
from django.http import HttpResponse, HttpResponseRedirect
import string
import random
from django.core import serializers
import constantsTheAyudar as consts
import smtplib
log = logging.getLogger(__name__)
USERNAME = "USERNAME"


def getSubscribedData(username,user_id):
    key=username+str(user_id)
    log.debug(key)
    subsData = cache.get(key)
    if subsData is None:
       subsData = UserEvents.objects.using('theayudar').filter(pk=user_id).all()
       log.debug("subsData is ")
       log.debug(subsData)       
       if len(subsData)<=0:
           return None
       else:
           cache.set(key,subsData,7200)
           return subsData
    else:
        return subsData
if __name__ == '__main__':
    print("using userDataOperations")
