# vim: set fileencoding=utf-8 :
"""
Models.
"""
from shared import db

# SQLAlchemy example
# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True)
#     pw_hash = db.Column(db.String(80))
#
#     def __init__(self, username, password):
#         self.username = username
#         self.set_password(password)
#
#     def set_password(self, password):
#         self.pw_hash = generate_password_hash(password)
#
#     def check_password(self, password):
#         return check_password_hash(self.pw_hash, password)
#
#     def __repr__(self):
#         return '<User %r>' % self.username
#
# To create tables:
# >>> from app import db
# >>> db.create_all()


# GAE example.
# For details, refer to
# `Google App Engine docs <http://code.google.com/appengine/docs/python/datastore/>`_::
#
# class Book(db.Model):
#     title = db.StringProperty(required=True)
#     summary = db.StringProperty()
#     authors = db.StringListProperty()
#     review = db.TextProperty()
#     synopsis = db.TextProperty()
#     cover = db.BlobProperty()
#     pub_date = db.DateProperty()
#     genre = db.CategoryProperty()
#     rating = db.Rating()
