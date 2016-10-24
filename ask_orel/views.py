from django.http import HttpResponse
#import datetime

def hello_world(request):
    #now = datetime.datetime.now()
    #html = "<html><body>It is now %s.</body></html>" % now

    data = '<p>Hello, world! </p>'\
    '<p>'+ request.method + ' ' + request.path + '</p>'
    return HttpResponse(data)
