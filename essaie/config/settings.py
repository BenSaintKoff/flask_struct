'''from cryptography.fernet import Fernet
key = b'pRmgMa8T0INjEAfksaq2aafzoZXEuwKI7wDe4c1F8AY='
crypto = Fernet(key)
f=open('./risque_backend/config/password','rb')
dec=crypto.decrypt(f.read()).decode('utf-8')'''


class BaseConfig():
   TESTING = False
   DEBUG = False


class DevConfig(BaseConfig):
   FLASK_ENV = 'development'
   DEBUG = True
   SECRET_KEY='9OLWxND4o83j4K4iuopO'
   #SQLALCHEMY_DATABASE_URI = 'postgres://postgres:%s@localhost/actions'%dec
   #SQLALCHEMY_DATABASE_URI = 'postgres://postgres:Abel1990@localhost/sentinelle'
   SQLALCHEMY_DATABASE_URI = 'postgres://postgres:Mpe.0123456789@localhost/angalia'

   #SQLALCHEMY_BINDS={'users':'sqlite:///db.sqlite'}
   FLASK_ADMIN_SWATCH='cerulean'
   TRACK_USAGE_USE_FREEGEOIP=False
   TRACK_USAGE_INCLUDE_OR_EXCLUDE_VIEWS='include'


class ProductionConfig(BaseConfig):
   FLASK_ENV = 'production'
   SECRET_KEY='9OLWxND4o83j4K4iuopO'
   #SQLALCHEMY_DATABASE_URI = 'postgres://postgres:%s@localhost/actions'%dec
   #SQLALCHEMY_DATABASE_URI = 'postgres://postgres:Abel1990@localhost/sentinelle'
   SQLALCHEMY_DATABASE_URI = 'postgres://postgres:Mpe.0123456789@localhost/angalia'

   #SQLALCHEMY_BINDS={'users':'sqlite:///db.sqlite'}
   FLASK_ADMIN_SWATCH='cerulean'
   TRACK_USAGE_USE_FREEGEOIP = False
   TRACK_USAGE_INCLUDE_OR_EXCLUDE_VIEWS = 'include'


class TestConfig(BaseConfig):
   FLASK_ENV = 'development'
   TESTING = True
   DEBUG = True


#uri='postgres://postgres:%s@localhost/actions'%dec
#uri='postgres://postgres:Abel1990@localhost/sentinelle'
uri='postgres://postgres:Mpe.0123456789@localhost/angalia'

