from os import environ

from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp import ApplicationError
from mongoengine import connect
from twisted.internet.defer import inlineCallbacks

from Models.User import User

connect(host=environ['MONGODB_URI'])


class AuthenticatorSession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        def authenticate(realm, authid, details):
            print("WAMP-CRA dynamic authenticator invoked: realm='{}', authid='{}'".format(realm, authid))
            user = User.objects(username=authid).first()
            if user:
                return {
                    'authid': str(user.id),
                    'secret': user.password,
                    'role': 'frontend',
                    'salt': user.username,
                    'iterations': 1000,
                    'keylen': 32
                }
            else:
                raise ApplicationError(u'com.example.no_such_user',
                                       'could not authenticate session - no such user {}'.format(authid))

        try:
            yield self.register(authenticate, u'authenticate')
            print("WAMP-CRA dynamic authenticator registered!")
        except Exception as e:
            print("Failed to register dynamic authenticator: {0}".format(e))
