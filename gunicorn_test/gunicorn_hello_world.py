def application(environ, start_response):
    #print(environ['HTTP_HOST'] + environ['RAW_URI'])

    path_info = environ['PATH_INFO']
    request_method = environ['REQUEST_METHOD']
    query_string = environ['QUERY_STRING']

    data = 'Hello, world!\n'\
    + path_info + '\n'\
    + request_method + ' ' + query_string + '\n'

    status = '200 OK'
    response_headers = [
        ('Content-Type','text/plain'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status, response_headers)
    return iter([data])
