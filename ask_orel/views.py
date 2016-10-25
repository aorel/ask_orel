from django.http import HttpResponse
#import datetime

def hello_world(request):
    #now = datetime.datetime.now()
    #html = "<html><body>It is now %s.</body></html>" % now

    data = '<p>1Hello, world! </p>'\
    '<p>'+ request.path + '</p>'\
    '<p>'+ request.method + ' ' + request.META['QUERY_STRING'] + '</p>'
    return HttpResponse(data)
