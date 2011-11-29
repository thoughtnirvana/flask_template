import datetime
import gevent
from flask import Response

def longpoll():
    def generate():
        yield ' ' * 1000
        yield "<html><body><h1>Current Time:</h1>"
        current = start = datetime.datetime.now()
        end = start + datetime.timedelta(seconds=60)
        while current < end:
            current = datetime.datetime.now()
            yield '<div>%s</div>' % current.strftime("%Y-%m-%d %I:%M:%S")
            gevent.sleep(1)

        yield '</body></html>'
    return Response(generate())
