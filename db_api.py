import sqlite3
import jsonpickle
import datetime
import json

def obj_dict(obj):
    return obj.__dict__

class Database():
    def __init__(self):
        self.conn = sqlite3.connect('database/selfpg.db')
        self.c = self.conn.cursor()
        self.create_table_parties()

    def select_last_entry(self):
        self.c.execute("SELECT parties FROM partystatus ORDER BY ROWID DESC LIMIT 1")
        output = self.c.fetchone()
        jout = output[0]
        #print (jout[0]["partyname"])
        return  (jout)


    def create_table_parties(self):
        self.c.execute("CREATE TABLE IF NOT EXISTS partystatus(time datetime(3), parties TEXT)")
        self.conn.commit()

    def insert_table_parties(self, partylist):
        self.c.execute("INSERT INTO partystatus(time, parties) VALUES (?, ?)",
            (datetime.datetime.now(), jsonpickle.dumps(partylist)))
        #print (jsonpickle.dumps(partylist))
        self.conn.commit()


if __name__ == '__main__':
    db = Database()
    output = db.select_last_entry()
    jout = output
    #print (jout)