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
        self.init_new_database()


    def init_new_database(self):
        self.ref.delete()


    def send_parties(self, partylist):
        parties_ref = self.ref.child('parties')
                
        for party in partylist:
            parties_ref.child(party.id).set({
                'id': party.id,
                'partyname': party.partyname,
                'members': [x.name for x in party.members],
                'position' : {
                    'lat': party.pos.x,
                    'lon': party.pos.y
                    },
                'activity' : str(party.activity),
                'gold': party.gold            
            })

    def send_towns(self, townlist):
        towns_ref = self.ref.child('towns')

        for town in townlist:
            towns_ref.child(town.id).set({
                'id': town.id,
                'name': town.name,
                'reputation': town.reputation,
                'gold': town.gold,
                'taxdays': town.day,
                'position' : {
                    'lat': town.pos.x,
                    'lon': town.pos.y
                    }
            })

    def store_tick(self, partylist, townlist):

        self.send_parties(partylist)
        self.send_towns(townlist)

        



