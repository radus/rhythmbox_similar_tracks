from gi.repository import GObject, RB, Peas, Gtk
from controller import SimilarTracksController


class SimilarTracksPlugin (GObject.Object, Peas.Activatable):
    object = GObject.property(type=GObject.Object)

    def __init__(self):
        super(SimilarTracksPlugin, self).__init__()

    def do_activate(self):
        self.controller = SimilarTracksController(self)
        self.controller.initialize()

    def do_deactivate(self):
        self.controller.cleanup()
