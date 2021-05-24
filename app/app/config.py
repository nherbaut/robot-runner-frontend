import os

basedir = os.path.abspath(os.path.dirname(__file__))


class DevConfig(object):
    pass


class ProdConfig(object):
    pass

env = os.environ.get("APP_ENV", "development")
print("[] environment : %s" % env)
if env == "production":
    config = ProdConfig()
else:
    config = DevConfig()
print("[] using %s config " % str(type(config)))
