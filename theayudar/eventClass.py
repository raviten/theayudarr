import django
import logging
from django.core.cache import cache
from theayudar.models import Eventinfo
from django.utils import timezone


log = logging.getLogger(__name__)
EVENTS_KEY = "EVENTS"

def getActiveEvents():
    events = cache.get(EVENTS_KEY)
    log.info("before memcache") 
    log.info(events)
    if events is None:
        log.debug("dbcall")
##        cur = django.db.connections['theayudar'].cursor()
##        cur.execute("SELECT * FROM ayudar.eventinfo where datetime > curtime()")
##        events = cur.fetchall()
##        #Clean-up after ourselves
##        cur.close()
        events = Eventinfo.objects.using('theayudar').filter(datetime__gt=timezone.now()).all()
        cache.set(EVENTS_KEY,events,6000000)
    else:
        log.debug("memcahhce")
##    for obj in events:
##        log.debug("object here")
##        k=Eventinfo(obj)
##        log.debug(k.name)
    return events
