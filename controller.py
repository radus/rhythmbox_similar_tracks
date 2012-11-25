from view import SimilarTracksView
from rbclasses import RBEntry
import lastfm
import rb_utils
import netlib

class SimilarTracksController:
    
    def __init__(self, plugin):
        self.plugin = plugin
        self.shell = plugin.object
        self.shell_player = self.shell.props.shell_player
        self.view = SimilarTracksView(plugin)
        self.cb_ids = ()
        self.current_artist = ""
        self.current_track = ""

    def initialize(self):
        self.connect_signals()
        self.view.show_ui()

    def connect_signals(self):
        self.cb_ids = (self.shell_player.connect('playing-changed',
                                                 self.playing_changed_cb),
                       self.shell_player.connect('playing-song-changed',
                                                 self.playing_changed_cb))

    def get_playing_entry(self):
        playing_entry = None
        if self.shell_player:
            playing_entry = self.shell_player.get_playing_entry()
        rb_entry = None
        if playing_entry is not None:
            rb_entry = RBEntry(playing_entry)
        return rb_entry

    def playing_changed_cb(self, playing, user_data):
        rb_entry = self.get_playing_entry()
        if rb_entry is None:
            return

        previous_artist = self.current_artist
        if previous_artist != rb_entry.artist:
            self.current_artist = rb_entry.artist
            self.update_similar_artists(rb_entry.artist)

        previous_track = self.current_track
        if previous_track != rb_entry.title:
            self.current_track = rb_entry.title
            self.update_similar_tracks(rb_entry.artist, rb_entry.title)

    def update_similar_artists(self, artist):
        self.view.clear_artists()
        print u"Update artists for {}".format(artist).encode("utf-8")
        if rb_utils.is_valid_artist(artist):
            self.load_similar_artists_async(artist)
        else:
            self.set_invalid_artist()

    def load_similar_artists_async(self, artist):
        lastfm.get_similar_artists_async(artist = artist,
                            success_callback = self.load_similar_artists_cb)

    def load_similar_artists_cb(self, similar_artists):
        
        rb_entry = self.get_playing_entry()
        if rb_entry.artist != similar_artists["artist_queried"]:
            #No need to do anything, the artist was changed
            return
        for artist in similar_artists['similars']:
            self.view.add_artist_without_image(artist)
            self.load_image_async(artist.image_url, 
                                  self.view.update_artist_image, artist.name)

    def update_similar_tracks(self, artist, track):
        self.view.clear_tracks()
        if rb_utils.is_valid_artist(artist):
            self.load_similar_tracks_async(artist, track)
        else:
            self.set_invalid_track()
    
    def load_similar_tracks_async(self, artist, track):
        lastfm.get_similar_tracks_async(artist = artist,
                                track = track,
                                success_callback = self.load_similar_tracks_cb)
    
    def load_similar_tracks_cb(self, similar_tracks):
        rb_entry = self.get_playing_entry()
        if rb_entry.title != similar_tracks["track_queried"]:
            return
        for track in similar_tracks['similars']:
            print("Adding track without image %s" % track.name) 
            self.view.add_track_without_image(track)
            self.load_image_async(track.image_url,
                                  self.view.update_track_image, track.name)

    def load_image_async(self, image_url, *params):
        """
        Sends response to function load_image_cb
        """
        print "reading image from url %s" % image_url
        netlib.get_url_async(image_url, self.load_image_cb, *params)

    def load_image_cb(self, image_data, view_callback, *params):
        """
        view_callback: function from view to update the image displayed.
        """
        image = rb_utils.get_image_pixbuf(image_data = image_data)
        view_callback(image, *params)
    def disconnect_signals(self):
        for cb in self.cb_ids:
            self.shell_player.disconnect(cb)

    def cleanup(self):
        self.disconnect_signals()
        self.view.destroy()
        del self.plugin
        del self.shell
        del self.shell_player
