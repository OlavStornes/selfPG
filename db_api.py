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

        # Initialise references
        self.parties_ref = self.ref.child('parties')
        self.towns_ref = self.ref.child('towns')
        self.members_ref = self.ref.child('members')
        
        
        

    def init_new_database(self):
        self.ref.delete()


    def send_parties(self, partylist):
                
        for party in partylist:
            


            self.send_members(party.members)
            self.parties_ref.child(party.id).set({
                'id': party.id,
                'partyname': party.partyname,
                'members': {x.id:True for x in party.members},
                'position' : {
                    'lat': party.pos.x,
                    'lon': party.pos.y
                    },
                'activity' : str(party.activity),
                'gold': party.gold            
            })

    def send_members(self, memberlist):
        for member in memberlist:
            self.members_ref.child(member.id).set({
                'id': member.id,
                'name': member.name,
                'maxHp': member.maxhp,
                'hp': member.hp,
                'lvl': member.lvl,
                'xp': member.exp,
                'nextLvl': member.nextlvl,
                'str': member.stronk,
                'int': member.smart,
                'partyid': member.party.id,
                'status': str(member.statuses)
            })


    def send_towns(self, townlist):

        for town in townlist:
            self.towns_ref.child(town.id).set({
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

        



