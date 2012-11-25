from gi.repository import Gtk, GdkPixbuf

class Artist(object):

    def __init__(self, init_data = None):
        self.name = ""
        self.image = ""
        self.image_url = ""
        if init_data is not None:
            self.update_data(init_data) 

    def update_data(self, field_values):
        if 'name' in field_values:
            self.name = field_values['name']
        if 'image' in field_values:
            self.image = field_values['image']
        if 'image_url' in field_values:
            self.image_url = field_values['image_url'] 
    
    def set_image_from_uri_data(self, image_data):
        loader = GdkPixbuf.PixbufLoader()
        loader.write(image_data)
        loader.close()
        self.image = loader.get_pixbuf()

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

