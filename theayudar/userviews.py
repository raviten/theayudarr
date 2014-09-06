from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.cache import never_cache
import django
import logging
from django.template import RequestContext, loader
import datetime
from django.core.context_processors import csrf
import userOperations
from theayudar.models import UserNormal,ERD
from django.core import serializers
import string
import random
import eventClass
import constantsTheAyudar as consts
import re
log = logging.getLogger(__name__)

@never_cache
def activate_account(request):
    status=userOperations.isAnonymous(request)
    if not status:
        details=userOperations.getUserData(request)
        log.debug(details)

        if details is not None and details['is_active']==0:
             email=details['email']
             log.debug(details['email'])
             log.debug(details['user_id'])
             resp=userOperations.sendEmail(email)
             if resp==1:
                 log.info("sent activation email to "+email)
                 return HttpResponse("A email has been sent to "+email+" please check the email or <br> \
                                     send a email to ismteja@gmail.com with your account for activation")
             elif resp==0:
                 return HttpResponse("There is a problem in sending email please try after 3 hours")
             else:
                return HttpResponse("email is already sent to "+str(email)+" please check in your inbox or spam folderor <br> \
                                     send a email to ismteja@gmail.com with your account for activation")
             return HttpResponse("There is a problem in sending email please try again")
        elif details is not None and details['is_active']==1:
            return HttpResponse("Your account is already activated")
                       
    else:
        return HttpResponseRedirect(consts.login)

@never_cache
def user_login(request):
    status=userOperations.isAnonymous(request)
    log.debug("user is anonymus "+str(status))
    if status:
        log.debug("user is anonymus"+str(status))
        log.debug(request.POST)
        if request.method == 'POST' and 'signIn' in request.POST:
            username = request.POST.get('Email',"None")
            password = request.POST.get('Passwd',"None")
            log.debug("password")
            log.debug(password)
            #This authenticates the user
            if username=="None" \
               or username.strip()==""\
               or password=="None"\
               or password.strip()=="":
                email=""
                if username!="None" :
                    email=username
                template = loader.get_template('theayudar/login.html')
                context = RequestContext(request, {
                'error_signin': "Wrong username/password",
                'errorType_signin':"alert-warning",
                'email':email,
                        })
                return HttpResponse(template.render(context))
            user = userOperations.authenticate(request,username=username, password=password)
            if user is not None:
                log.debug("is user active "+str(user['is_active']))
                log.debug(str(user))
                #This logs him in
                name=user['first_name']+" "+user['last_name']
                template = loader.get_template('theayudar/index.html')
                context = RequestContext(request, {
                      'name': name,
                      'signin':1,
                      'name':name,
                      'active':user['is_active'],
                  })
                response=HttpResponse(template.render(context))
                response = userOperations.login(response,user['uid'],user['email'])
                log.info("LOGIN:username::"+username)
                return response
            else:
                template = loader.get_template('theayudar/login.html')
                context = RequestContext(request, {
                'error_signin': "Wrong username/password",
                'errorType_signin':"alert-warning",
                'email':username,
                        })
                return HttpResponse(template.render(context))
        elif request.method=='POST' and 'signUp' in request.POST:
            fName = request.POST.get('f_name','default')
            lName = request.POST.get('l_name','default')
            email = request.POST.get('email','default')
            password = request.POST.get('s_password','default')
            repassword=request.POST.get('sv_password','default')
            log.debug("fname is ::"+fName);
            if fName=='default' or fName.strip()=="" \
               or lName=='default' or lName.strip()=="" \
               or email=='default' or email.strip()=="" \
               or password=='default' or password.strip()=="" \
               or repassword=='default' or repassword.strip()=="" \
                :
                              
                template = loader.get_template('theayudar/login.html')
                context = RequestContext(request, {
                'error_signup': "please verify details..All Fields are mandatory",
                        })
                return HttpResponse(template.render(context))
            if password != repassword:
                template = loader.get_template('theayudar/login.html')
                context = RequestContext(request, {
                'error_signup': "Passwords must match",
                        })
                return HttpResponse(template.render(context))
            
            if len(password)>=8 and password.isalnum():
                pass
            else:
                template = loader.get_template('theayudar/login.html')
                context = RequestContext(request, {
                'error_signup': "Passwords must contain only numbers and digits and length more than 8",
                        })
                return HttpResponse(template.render(context))
            if userOperations.checkUserExists(email):
                template = loader.get_template('theayudar/login.html')
                context = RequestContext(request, {
                'error_signup': "username already exists",
                        })
                return HttpResponse(template.render(context))
            else:
                userOperations.signUp(request,fName,lName,email,password)
                user = userOperations.authenticate(request,username=email, password=password)
                response = userOperations.login(request,user)
                return response
        elif request.method == 'GET':
          log.debug("inside post methd")
          template = loader.get_template('theayudar/login.html')
          c = {}
          c.update(csrf(request))
          context = RequestContext(request)
          response=HttpResponse(template.render(context))
          response.delete_cookie("uid")
          response.delete_cookie("email")
          return response
        else:
            return HttpResponseRedirect(consts.errorPage)
    else:
        return  HttpResponseRedirect(consts.myprofile)

    
@never_cache
def user_logout(request):
  template = loader.get_template('theayudar/logout.html')
  context = RequestContext(request, {
                'response': "You have been succesfully logged out",
                        })
  userOperations.logout(request)
  response = HttpResponse(template.render(context))
  response.delete_cookie("uid")
  response.delete_cookie("email")
  return response

@never_cache
def user_info(request):
  status=userOperations.isAnonymous(request)
  if status:
    return HttpResponseRedirect(consts.login)
  else:
    details=userOperations.getUserData(request)
    log.debug(details)

    if details is not None:
         log.debug(details['email'])
         log.debug(details['user_id'])
         data=None
         if details['is_active']==1:
             log.debug("inside")
             data = userOperations.getCompletedData(details['user_id'])
         resp=""
         log.debug(data)
         if data is None:
             resp="Please join and complete one of the event"
         template = loader.get_template('theayudar/userprofile.html')
         context = RequestContext(request, {
                'response': resp,
                'name':details['first_name']+" "+details['last_name'],
                'points':details['points'],
                'active':details['is_active'],
                'email':details['email'],
                'data':data,
                
                        })  
         return  HttpResponse(template.render(context))
    else:
        template = loader.get_template('theayudar/error.html')
        context = RequestContext(request, {
                'response': "Some thing went wrong...",
                        })
        return  HttpResponse(template.render(context))

@never_cache
def participatingEvents(request):
  status = userOperations.isAnonymous(request)
  if status:
    return HttpResponseRedirect(consts.login)
  else:
    details=userOperations.getUserData(request)
    log.debug(details)

    if details is not None:
         log.debug(details['email'])
         log.debug(details['user_id'])
         data = userOperations.getSubscribedData(details['email'],details['user_id'])
         events=eventClass.getActiveEvents().filter(event_id__in = data.values('event_id'))
         log.debug(events)
         response="";
         subs=0
         if data is None or len(data)==0 and details['is_active']==1:
             response = "you haven't subscribed to any of the events"
             subs=1
         template = loader.get_template('theayudar/subscribedevents.html')
         context = RequestContext(request, {
                'response': response,
                'name':details['first_name']+" "+details['last_name'],
                'points':details['points'],
                'active':details['is_active'],
                'events':events,
                'subs':subs,
                        })
         return  HttpResponse(template.render(context))
    else:
        template = loader.get_template('theayudar/error.html')
        context = RequestContext(request, {
                'response': "Some thing went wrong...",
                        })
        return  HttpResponse(template.render(context))

@never_cache
def upcomingevents(request):
  log.debug(request)
  status = userOperations.isAnonymous(request)
  if status:
       responseVal=""
       template = loader.get_template('theayudar/notloggedinevents.html')
       events = eventClass.getActiveEvents()
       context = RequestContext(request, {
                'events':events,
                'response': responseVal,
                'responseType':"",
                'signin':'0',
                        })
       return  HttpResponse(template.render(context))
    
  else:
    details=userOperations.getUserData(request)
    log.debug(details)

    if details is not None:
         log.debug(details['email'])
         log.debug(details['user_id'])
         data = userOperations.getSubscribedData(details['email'],details['user_id'])
         ##need to write function for fetching events in a proper way
         events = eventClass.getActiveEvents().exclude(event_id__in = data.values('event_id'))
         log.debug(events)
         log.debug(data)
         if data is None:
             data=[]
         template = loader.get_template('theayudar/events.html')
         responseVal=""
         if len(events) == 0:
             responseVal="There are no upcoming events..U are so good That u are willing to help people at your full capacity"
         context = RequestContext(request, {
                'response': responseVal,
                'name':details['first_name']+" "+details['last_name'],
                'points':details['points'],
                'active':details['is_active'],
                'events':events,
                'subscribeddata':data,
                        })
         return  HttpResponse(template.render(context))
    else:
        template = loader.get_template('theayudar/error.html')
        context = RequestContext(request, {
                'response': "Some thing went wrong...",
                        })
        return  HttpResponse(template.render(context))

##need to optimize the database calls
@never_cache
def registerEvent(request):
  status = userOperations.isAnonymous(request)
  #validating a positive integer for event
  eid=request.GET.get('eid',-1)
  if eid ==-1 or not eid.isdigit():
     log.debug("no event id is produced")
     log.debug(eid)
     return HttpResponseRedirect(consts.login)
  if status:
    events = eventClass.getActiveEvents()  
    return HttpResponseRedirect(consts.login)
  else:
    details=userOperations.getUserData(request)
    log.debug(details)
    if details is not None and details['is_active']==0:
        events = eventClass.getActiveEvents()
        template = loader.get_template('theayudar/events.html')
        context = RequestContext(request, {
##           'response': "you have already subscribed to event ",#+str(e[0].name),
           'name':details['first_name']+" "+details['last_name'],
           'points':details['points'],
           'active':details['is_active'],
           'events':events,
                   })
        return  HttpResponse(template.render(context))
    elif details is not None and details['is_active']==1:
         log.debug(details['email'])
         log.debug(details['user_id'])
         events = eventClass.getActiveEvents()
         data = userOperations.getSubscribedData(details['email'],details['user_id'])
         log.debug(data)
         log.debug(data.filter(event_id=eid))
         e = events.filter(event_id=eid)
         if len(e)==0:
             if len(data)!=0:
                 events=events.exclude(event_id__in = data.values('event_id'))
             template = loader.get_template('theayudar/events.html')
             context = RequestContext(request, {
                'response': "No such event exists",#+str(e[0].name),
                'responseval':"warning",
                'name':details['first_name']+" "+details['last_name'],
                'points':details['points'],
                'active':details['is_active'],
                'events':events,
                        })
             return  HttpResponse(template.render(context))
         elif len(data)!=0 and len(data.filter(event_id=eid))!=0:
                log.debug(data)
                log.debug("123")
                log.debug(events)
                events=events.exclude(event_id__in = data.values('event_id'))
                log.debug(events)
                template = loader.get_template('theayudar/events.html')
                context = RequestContext(request, {
                'response': "you have already subscribed to event ",#+str(e[0].name),
                'responseval':"info",
                'name':details['first_name']+" "+details['last_name'],
                'points':details['points'],
                'active':details['is_active'],
                'events':events,
                        })
                return  HttpResponse(template.render(context))
         eventReg = userOperations.reg(details['email'],details['user_id'],eid)
         log.info(details['email']+" registers for the event "+str(eid))
         ##need to write function for fetching events in a proper way
         data = userOperations.getSubscribedData(details['email'],details['user_id'])
##         log.debug(events)
##         log.debug(data)
         if data is None:
             data=[]
         else:
            events=events.exclude(event_id__in = data.values('event_id'))
         template = loader.get_template('theayudar/events.html')
         context = RequestContext(request, {
                'response': "succesfully registered to event "+str(e[0].name),
                'responseval':"success",
                'name':details['first_name']+" "+details['last_name'],
                'points':details['points'],
                'active':details['is_active'],
                'events':events,
                'subscribeddata':data,
                        })
         return  HttpResponse(template.render(context))
    else:
        template = loader.get_template('theayudar/error.html')
        context = RequestContext(request, {
                'response': "Some thing went wrong...",
                        })
        return  HttpResponse(template.render(context))



##def set_cookie(response, key, value, days_expire = 7):
##  if days_expire is None:
##    max_age = 365 * 24 * 60 * 60  #one year
##  else:
##      max_age = days_expire * 24 * 60 * 60 
##  expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
##  response.set_cookie(key, value, max_age=max_age, expires=expires)
##  return response

##def signup(request):
##  if request.session.get('signin',True):
##    username="raviteja"
##    log.debug(request.session.get('signin',True))
##    log.debug(username)
##    log.info('username'+username)
##    log.debug("already signed in")
##    return HttpResponse("you re already signed in")
##  elif request.method=="GET":
##    template = loader.get_template('theayudar/signin.html')
##  else:
##    if request.method=="POST":
##        log.debug("inside post method")
##        username = request.POST["username"]
##        password = request.POST["password"]
##        user = userOperations(username)
##        if user is None:
##          return HttpResponse("User name or Password is invalid")
##        response = HttpResponse("your reequest is bieng processed")
##        response=set_cookie(response,'email', str(username))
##        request.session.set('signin',True)
##        request.session.set('email',email)
##        log.debug(email)
##        reurn response
##    else:
##        response = HttpResponse("please use post method")
##        return response
##  
##def user_login(request):
##    if request.user.is_anonymous():
##        log.info("user is anonymus")
##        if request.method == 'POST':
##            username = request.POST['username']
##            password = request.POST['password']
##            #This authenticates the user
##            user = authenticate(username=username, password=password)
##            if user is not None:
##                if user.is_active:
##                    #This logs him in
##                    login(request, user)
##                else:
##                    return HttpResponse("Not active")
##            else:
##                return HttpResponse("Wrong username/password")
##    return HttpResponseRedirect("/theayudar/")
##
### User Logout View
##def user_logout(request):
##    logout(request)
##    return HttpResponseRedirect('/')
##
### User Register View
##def user_register(request):
##    if request.user.is_anonymous():
##        if request.method == 'POST':
##            form = UserRegisterForm(request.POST)
##            if form.is_valid:
##                form.save()
##                return HttpResponse('User created succcessfully.')
##        else:
##            form = UserRegisterForm()
##        context = {}
##        context.update(csrf(request))
##        context['form'] = form
##        #Pass the context to a template
##        return render_to_response('register.html', context)
##    else:
##        return HttpResponseRedirect('/')
