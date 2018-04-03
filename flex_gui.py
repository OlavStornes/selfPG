
from time import time
import psutil
import asyncio
from flexx import app, event, ui, config, util
from leafgui import *
from exampledata import xdat

xdata = xdat

def get_mapname():
    namelist = []
    for index, party in enumerate(xdat):
        namelist.append(xdat[index]["partyname"])
    return namelist

class Overview(ui.Widget):
    def init(self):
        self.combo = ui.ComboBox(
            editable=True,
            options=(get_mapname())
        )

        self.label = ui.Label()
        with ui.FormLayout() as self.partystats:
            self.b1 = ui.Label(title='Name: ')
            self.b2 = ui.Label(title="Position: ")
            self.b3 = ui.Label(title="Gold: ")
            ui.Widget(flex=1)  # Spacing




    @event.reaction
    def update_label(self):
        if self.combo.selected_index is not -1:
            x = self.combo.selected_index
            self.b1.set_text(xdat[x].partyname)
            pos = str(xdat[x].pos.x) +", "+ str(xdat[x].pos.y)
            self.b2.set_text(pos)
            self.b3.set_text(xdat[x].gold)
            

class Leafmap(leaflet.LeafletExample):
    def init(self):
        with ui.HBox():
            self.leaflet = leaflet.LeafletWidget(
                flex=1,
                center=(52, 4.1),
                zoom=12,
                show_scale=lambda: self.cbs.checked,
                show_layers=lambda: self.cbl.checked,
            )

class Mainmap(ui.CanvasWidget):
    def init(self):
        super().init()

        self.ctx = self.node.getContext('2d')
        self.set_capture_mouse(1)
        self._last_pos = (0, 0)
        self.pos = {"x": 0, "y":0}

    @event.reaction('mouse_down')
    def on_down(self, *events):
        self.ctx.clearRect(0, 0, 1000, 1000)
        self.ctx.strokeRect(self.pos["x"], self.pos["y"],75,75)
        self.pos["x"] += 30

class MultiApp(ui.TabLayout):
    def init(self):
        Overview(title='Test')
        Mainmap(title='Main map')
        ui.YoutubeWidget(title='utubs', source="AqbLNXcITcU")
        Leafmap("whodis")

    def init_leaflet(self, title):
        leaf = leaflet.LeafletExample(title=title)
        leaf.leaflet.remove_layer('http://a.tile.openstreetmap.org/', 'OpenStreetMap')

        return leaf
        




if __name__ == '__main__':
    config.hostname = "0.0.0.0"
    app.launch(MultiApp, 'app')  # for use during development
    #app.start()
    app.run()

    