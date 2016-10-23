#gunicorn --config=getting_started/gunicorn_config.py ask_orel.wsgi

#gunicorn --config=gunicorn_config.py gunicorn_hello_world:app
#http://127.0.0.1:8081/lol.html?a=5&b=1

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
