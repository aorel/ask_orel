def app(environ, start_response):
    print(environ['HTTP_HOST'] + environ['RAW_URI'])

    request_method = environ['REQUEST_METHOD']
    raw_uri = environ['RAW_URI']

    data = 'Hello, world!\n'\
    + request_method + ' ' + raw_uri + '\n'

    status = '200 OK'
    response_headers = [
        ('Content-type','text/plain'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status, response_headers)
    return iter([data])
