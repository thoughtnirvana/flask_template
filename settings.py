"""
Default settings supported by Flask. Additional keys can be put
in here which will be accessible in `app.config` dictionary like
object.
"""
#: Dev setup. Enable debugger.
DEBUG = True
#: Enable testing for development.
TESTING = False
#: Enable CSRF. Might not be needed if WTForms is used.
CSRF_ENABLED = True
#: Key for CSRF.
CSRF_SESSION_LKEY = '\x126S{\x94\xbf}o5YE\xac\x17\x8e8^_\x18z\x08\xf3z1\x97'
#: Session signing key.
SECRET_KEY = '\x18[F;(\x99\xbcF\xc8\xe3\xb5\x89R\xb7[\x17H\x85\xd8\xa9,\xbf\x95\xb4;\xe1\x80\x872+\x82\x93'
#: If web server supports it, directly send the static files from webserver.
USE_X_SENDFILE = True
#: Cache type. Used by Flask-Cache extension.
CACHE_TYPE = 'simple'
#: Database to use for SQLAlchemy.
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
