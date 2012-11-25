from gi.repository import RB

class RBEntry:
    
    def __init__(self, entry):
        self.artist = entry.get_string(RB.RhythmDBPropType.ARTIST)
        self.title = entry.get_string(RB.RhythmDBPropType.TITLE)


class Artist(object):

    def __init__(self, init_data = None):
        self.name = ""
        self.image_url = ""
        if init_data is not None:
            self.update_data(init_data) 

    def update_data(self, field_values):
        if 'name' in field_values:
            self.name = field_values['name']
        if 'image_url' in field_values:
            self.image_url = field_values['image_url'] 
    

class SimilarArtist(Artist):

    def __init__(self, init_data = None):
        super(SimilarArtist, self).__init__(init_data)
        self.similarity = 0
        if init_data is not None:
            self.update_data(init_data)

    def update_data(self, field_values):
        super(SimilarArtist,self).update_data(field_values)
        if 'similarity' in field_values:
            self.similarity = field_values['similarity']


class Track(object):
    
    def __init__(self, init_data = None):
        self.name = ""
        self.artist = ""
        self.image_url = ""
        if init_data is not None:
            self.update_data(init_data)

    def update_data(self, field_values): 
        if 'name' in field_values:
            self.name = field_values['name']
        if 'image_url' in field_values:
            self.image_url = field_values['image_url']
        if 'artist' in field_values:
            self.artist = field_values['artist']


class SimilarTrack(Track):

    def __init__(self, init_data = None):
        super(SimilarTrack, self).__init__(init_data)
        self.similarity = 0
        if init_data is not None:
            self.update_data(init_data)

    def update_data(self, field_values):
        super(SimilarTrack, self).update_data(field_values)
        if 'similarity' in field_values:
            self.similarity = field_values['similarity']
