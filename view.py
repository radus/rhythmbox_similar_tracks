from gi.repository import RB, Gtk
import os

UI_DIR = "ui"

class SimilarTracksView:
    
    def __init__(self, plugin):
        self.plugin = plugin

        self.artist_container = Gtk.VBox()
        self.tracks_container = Gtk.VBox()
        self.main_frm = Gtk.ScrolledWindow()

        # keeps a map between artist name and builder for 
        # widget that displays it
        self.artist_widgets = {}
        self.track_widgets = {}

    def show_ui(self):
        shell = self.plugin.object

        notebook = Gtk.Notebook()
        artists_lbl = Gtk.Label("Artists")
        notebook.append_page(self.artist_container, artists_lbl)
        tracks_lbl = Gtk.Label("Tracks")
        notebook.append_page(self.tracks_container, tracks_lbl)

        frame = Gtk.Frame()
        frame.set_label("Similar")
        frame.add(notebook)
        self.main_frm.add_with_viewport(frame)

        shell.add_widget(self.main_frm, RB.ShellUILocation.RIGHT_SIDEBAR, 
                         True, True)
        self.main_frm.show_all()
        self.main_frm.set_size_request(200, -1)

    def load_ui(self, ui_path):
        plugin_dir = self.plugin.plugin_info.get_data_dir()
        full_ui_path = os.path.join(plugin_dir, UI_DIR, ui_path + ".glade")
        builder = Gtk.Builder()
        builder.add_from_file(full_ui_path)
        return builder
    
    def info_widget_builder(self):
        builder = self.load_ui("InfoWidget")
        return builder

    def create_info_widget_builder(self, info, similarity):
        builder = self.info_widget_builder()
        info_lbl = builder.get_object("info_lbl")
        info_lbl.set_text(info)

        similarity_lbl = builder.get_object("similarity_lbl")
        text = "Similarity: {:.2%}".format(similarity)
        similarity_lbl.set_text(text)

        return builder

    def add_artist_without_image(self, artist):
        """
        Adds a new artist, without the image.
        """
        print u"Adding artist {}".format(artist.name).encode("utf-8")

        builder = self.create_info_widget_builder(artist.name, 
                                                  artist.similarity)

        self.artist_widgets[artist.name] = builder
        artist_widget = builder.get_object("info_widget")
        self.artist_container.pack_start(artist_widget, False, False, 0)

    def update_artist_image(self, image, artist):
        """
        artist = artist name as string
        """
        if not (artist in self.artist_widgets):
            return
        image_widget = self.artist_widgets[artist].get_object("img")
        image_widget.set_from_pixbuf(image)

    def clear_artists(self):
        self.artist_widgets.clear()
        self.artist_container.foreach(self.destroy_widget, None)

    def add_track_without_image(self, track):
        track_string = track.artist + "-" + track.name
        builder = self.create_info_widget_builder(track_string, 
                                                  track.similarity)
        self.track_widgets[track.name] = builder
        track_widget = builder.get_object("info_widget")
        self.tracks_container.pack_start(track_widget, False, False, 0)

    def update_track_image(self, image, track):
        if not (track in self.track_widgets):
            return
        track_widget = self.track_widgets[track].get_object("img")
        track_widget.set_from_pixbuf(image)

    def clear_tracks(self):
        self.track_widgets.clear()
        self.tracks_container.foreach(self.destroy_widget, None)

    def destroy_widget(self, widget, data):
        widget.destroy()

    def destroy(self):
        shell = self.plugin.object
        shell.remove_widget(self.main_frm, RB.ShellUILocation.RIGHT_SIDEBAR)
        del self.plugin

