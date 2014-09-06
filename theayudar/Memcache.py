import memcache

mcSessions = memcache.Client(['127.0.0.1:11211'], debug=0)
##mcData = memcache.Client(['127.0.0.1:11212'], debug=0)
mcSessions.flush_all()
##mcData.flush_all()
