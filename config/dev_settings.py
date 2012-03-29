#: Dev setup. Enable debugger.
DEBUG = True
#: Enable testing for development.
TESTING = True
#: Database to use for SQLAlchemy.
SQLALCHEMY_DATABASE_URI = 'sqlite:///tmp/dev.db'

USE_X_SENDFILE = False
CACHE_TYPE = 'simple'

#: webassets settings.
ASSETS_DEBUG = True
