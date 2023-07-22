import requests

#Singleton
class Session(object):
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(Session, self).__new__(self)
            self.session = requests.Session()
        return self.instance
    def get_session(self):
        return self.session
    

