#!/usr/bin/env python
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import main

# Initialize app and serve.
http_server = HTTPServer(WSGIContainer(main.init()))
http_server.listen(8080)
IOLoop.instance().start()
