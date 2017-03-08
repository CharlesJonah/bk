import os
class Config(object):

    CSRF_ENABLED = True
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]

class Test(object):
    CSRF_ENABLED = True
    SQLALCHEMY_TEST_DATABASE_URI = os.environ["SQLALCHEMY_TEST_DATABASE_URI"]
    SECRET_KEY = os.environ["SECRET_KEY"]


