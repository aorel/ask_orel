#gunicorn --config=gunicorn_config.py gunicorn_hello_world:app
#http://127.0.0.1:8081/lol.html?a=5&b=1
def app(environ, start_response):
    print(environ['HTTP_HOST'] + environ['RAW_URI'])

    http_host = environ['HTTP_HOST']
    request_method = environ['REQUEST_METHOD']
    query_string = environ['QUERY_STRING']
    server_protocol = environ['SERVER_PROTOCOL']
    raw_uri = environ['RAW_URI']
    data = 'Hello, world!\n'\
    + request_method + ' ' + raw_uri + ' ' + server_protocol + '\n'
    #+ 'Host: ' + http_host + '\n'\
    #+ 'Query_string: ' + query_string + '\n'

    status = '200 OK'
    response_headers = [
        ('Content-type','text/plain'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status, response_headers)
    return iter([data])
