# -*- coding: cp1252 -*-
import django
import logging
from django.utils import timezone
from django.core.cache import cache
from theayudar.models import UserNormal,ERD,UCE
from django.http import HttpResponse, HttpResponseRedirect
import string
import random
from django.core import serializers
import constantsTheAyudar as consts
import smtplib
log = logging.getLogger(__name__)
USERNAME = "USERNAME"

def isAnonymous(request):
    log.debug("checking wether he is anonymus or not")
    uid = request.COOKIES.get("uid")
    if uid is None or len(uid)<32:
        return True
    log.debug("cookie is "+str(uid))
    username=request.COOKIES.get("email")
    log.debug("username is "+str(username))
    log.debug(username)
    if username is None or  len(username)<3:
        return True
    user=cache.get(username)
    log.debug(user)
    if user is None:
        userdetails = UserNormal.objects.using('theayudar').filter(username=username).all()
        if len(userdetails)>0:
            userD=userdetails[0];
            data ={'email':userD.email,'user_id':userD.user_id,'is_active':userD.is_active,'points':userD.points,\
                  'first_name':userD.first_name,'last_name':userD.last_name,'uid':userD.session_id,'last_login':userD.last_login}
            tm=(timezone.now()-data['last_login']).total_seconds()
            cache.set(username,data,tm)
            if tm<=7200 and uid==userD.session_id:
                return False
            else:
                return True
        else:
            return True
    else:
        tm=(timezone.now()-user['last_login']).total_seconds()
        if user['uid']==uid and tm<=7200:
            log.debug(tm)
            return False
        else:
            cache.delete(username)
            return True
def checkUserExists(email):
       userdetails = UserNormal.objects.using('theayudar').filter(username=email).all()
       log.debug(userdetails)
       if len(userdetails)<=0:
           return False
       else:
           return True
def signUp(request,fname,lname,email,password):
    user = UserNormal(password=password,username=email,email=email,first_name=fname,last_name=lname)
    user.save(using='theayudar')    

def authenticate(request,username,password):
    userdetails = UserNormal.objects.using('theayudar').filter(username=username).all()
    log.debug(len(userdetails))
    log.debug(userdetails)
    if len(userdetails)<=0 or (len(userdetails)>0 and userdetails[0].password!=password) :
        return None
    userD = userdetails[0]
    value=id_generator()
    data ={'email':userD.email,'user_id':userD.user_id,'is_active':userD.is_active,'points':userD.points,\
           'first_name':userD.first_name,'last_name':userD.last_name,'uid':value,'last_login':timezone.now()}
    userdetails.update(session_id=value);
    cache.set(username,data,7200)
    return data
def id_generator(size=32, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

def login(response,uid,email):
  response.set_cookie("uid", uid, max_age=None, expires=None, path='/', domain=None, secure=None, httponly=False)
  response.set_cookie("email", email, max_age=None, expires=None, path='/', domain=None, secure=None, httponly=False)
  return response
def getUserData(request):
    username = request.COOKIES.get("email")
    userD = cache.get(username)
    if userD is None:
        return None
    else:
        return userD
def logout(request):
    uid = request.COOKIES.get("uid")
    if uid is not None:
        cache.delete(uid)

def reg(username,user_id,eid):
    key=username+str(user_id)
    cache.delete(key)
    subevent = ERD(user_id=user_id,event_id=eid)
    subevent.save(using='theayudar')    
    log.debug(key)

def getSubscribedData(username,user_id):
    key=str(user_id)+username
    log.debug(key)
    subsData = cache.get(key)
    if subsData is None:
       subsData = ERD.objects.using('theayudar').filter(user_id=user_id).all()
       log.debug("subsData is ")
       log.debug(subsData)       
       if len(subsData)<=0:
           return subsData
       else:
           cache.set(key,subsData,1800)
           log.debug(subsData)
           return subsData
    else:
        return subsData
def getCompletedData(user_id):
    key=str(user_id)+"subscribed"
    log.debug(key)
    compData = cache.get(key)
    if compData is None:
       compData = UCE.objects.using('theayudar').filter(user_id=user_id).all()
       log.debug("compData is ")
       log.debug(compData)       
       if len(compData)<=0:
           return compData
       else:
           cache.set(key,compData,1800)
           return compData
    else:
        return compData    
def sendEmail(email):
    key="emailActivation"+email
    log.debug("key for sending activation mail "+key)
    emailKey = cache.get(key)
    log.debug("email key is ")
    log.debug(emailKey)
    if emailKey is None:
            rndm=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(34))
            while cache.get(rndm) is not None:
                  rndm=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(34))              
            url = 'http://'+str(consts.current_activation)+'?activation_rndm='+rndm
            gmail_user = consts.auth_user
            gmail_pwd = consts.auth_pass
            FROM = consts.from_user
            TO = [email] #must be a list
            SUBJECT = "Activate your Ayudar account"
            TEXT = "For better of people and next generation please use the below link .This link expires in 2 hours <br> "+url

            # Prepare actual message
            message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
            try:
                #server = smtplib.SMTP(SERVER) 
##                server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
##                server.ehlo()
##                server.starttls()
##                server.login(gmail_user, gmail_pwd)
##                server.sendmail(FROM, TO, message)
##                #server.quit()
##                server.close()
                cache.set(rndm,email,10800)
                cache.set(key,"1",10800)
                return 1
            except:
                return 0
    else:return -1
if __name__ == '__main__':
    print("using userOperations")
    ##def getUser(username):
##    userdetails = cache.get(USERNAME)
##    log.info("before memcache") 
##    log.info(events)
##    if events is None:
##        log.debug("dbcall")
####        cur = django.db.connections['theayudar'].cursor()
####        cur.execute("SELECT * FROM ayudar.eventinfo where datetime > curtime()")
####        events = cur.fetchall()
####        #Clean-up after ourselves
####        cur.close()
##        userdetails = UserNormal.objects.using('theayudar').filter(username=username).all()
##        if userdetails is None:
##            return None
##        for u in userdetails:
##            cache.set(USERNAME,u,6000000)
##    else:
##        log.debug("memcahhce")
##    for obj in userdetails:
##        log.debug("object here")
##        k=UserNormal(obj)
##        log.debug(k.first_name+" "+k.last_name)
##        return k
