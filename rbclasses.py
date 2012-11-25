from gi.repository import RB

class RBEntry:
    
    def __init__(self, entry):
        self.artist = entry.get_string(RB.RhythmDBPropType.ARTIST)
        self.title = entry.get_string(RB.RhythmDBPropType.TITLE)
