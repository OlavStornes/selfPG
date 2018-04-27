import firebase_admin
from firebase_admin import credentials, db

import jsonpickle
import datetime
import json


def obj_dict(obj):
    return obj.__dict__

class Firebase():
    def __init__(self):
        cred = credentials.Certificate('./api_key/self-pg-firebase-adminsdk.json')
        opt = {'databaseURL': 'https://self-pg.firebaseio.com/'}
        self.default_app = firebase_admin.initialize_app(cred, opt)

    def store_tick(self, partylist):
        ref = db.reference()
        parties_ref = ref.child('parties')


        jsonlist = jsonpickle.encode(party, unpicklable=True, max_depth=2)

        parties_ref.set(jsonlist)


