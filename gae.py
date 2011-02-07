"""
Creates the flask wsgi `app` and passes it on to gae wsgi
handler to run the application.
"""
#: stdlib imports
import os
#: 3rd party imports.
from google.appengine.ext.webapp.util import run_wsgi_app
import app

# Run the Flask wsgi `app`.
app = app.init()


def main():
    global app
    run_wsgi_app(app)


if __name__ == '__main__':
    main()
