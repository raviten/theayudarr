from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.cache import cache_control
import django
import logging
import eventClass
from theayudar.models import Eventinfo
from django.template import RequestContext, loader
import datetime
import userOperations
from django.core.context_processors import csrf
import constantsTheAyudar as consts


log = logging.getLogger(__name__)

def set_cookie(response, key, value, days_expire = 7):
  if days_expire is None:
    max_age = 365 * 24 * 60 * 60  #one year
  else:
      max_age = days_expire * 24 * 60 * 60 
  expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
  response.set_cookie(key, value, max_age=max_age, expires=expires)
  return response

def eventdetail(request,event_id):
  template = loader.get_template('theayudar/popEvent.html')
  events = Eventinfo.objects.using('theayudar').filter(event_id=event_id)
  if len(events)<=0:
    return HttpResponse("event doesn't exist")
  context =RequestContext(request, {
                'ev': events[0],
                        })
  return HttpResponse(template.render(context))

def test_count_session(request):
    if request.session.get('has_commented', False):
        return HttpResponse("You've already commented.")
    request.session['has_commented'] = True
    return HttpResponse('Thanks for your comment!')
@cache_control(must_revalidate=True, max_age=0)
def index(request):
##    events= EventObject.objects.all()
##    template = loader.get_template('ayudar/index.html')
##    context = RequestContext(request, {
##        'events': events,
##    })
##    log.debug("Hey there it works!!")
##    log.info("Hey there it works!!")
##    log.warn("Hey there it works!!")
##    log.error("Hey there it works!!")
##    events = Eventinfo.objects.using('theayudar').all()
    status=userOperations.isAnonymous(request)
    if status:
      events = eventClass.getActiveEvents()
      log.debug(events)
      for obj in events:
          log.debug(obj.name)
      template = loader.get_template('theayudar/index.html')
      context = RequestContext(request, {
          'events': events,
      })
      log.debug("hello")
      return HttpResponse(template.render(context))
    else:
      details=userOperations.getUserData(request)
      ############################################################
      #why are you doing this as anonnymus check is already done##
      if details is None:
        userOperations.logout(request)
        return HttpResponseRedirect(consts.login)
      ############################################################
      name=details['first_name']+" "+details['last_name']
      template = loader.get_template('theayudar/index.html')
      context = RequestContext(request, {
          'name': name,
          'signin':1,
          'name':name,
          'active':details['is_active'],
      })
      return HttpResponse(template.render(context))
def alreadySignedin(request):
  if request.session.get('signin',True):
    email = request.session.get('email')
    log.debug(email)
    return redirectHomePage(request,email)
  else:
    response = signin(request)
    return response
def signin(request):
    if request.method=="POST":
        log.debug("inside post method")
        email = request.POST["email"]
        response = HttpResponse("your reequest is bieng processed")
        response=set_cookie(response,'email', str(email))
        request.session.set('signin',True)
        request.session.set('email',email)
        log.debug(email)
        return response
    else:
        template = loader.get_template('theayudar/signin.html')
        c = {}
        c.update(csrf(request))
        context = RequestContext(request,c)
        return HttpResponse(template.render(context))

def indexredirect(request):
    return HttpResponseRedirect(consts.index)
