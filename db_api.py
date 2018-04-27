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
        self.ref = db.reference()


    def send_parties(self, partylist):
        parties_ref = self.ref.child('parties')
                
        for party in partylist:
            parties_ref.child(party.partyname).set({
            'members': [x.name for x in party.members],
            "position" : {
                "lat": party.pos.x,
                "lon": party.pos.y},
            "activity" : str(party.activity),
            "gold": party.gold            
            })

    def store_tick(self, partylist):

        self.send_parties(partylist)

        



