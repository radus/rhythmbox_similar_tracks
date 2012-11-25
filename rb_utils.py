from gi.repository import GdkPixbuf

def is_valid_artist(artist):
    if artist is not None and artist != "" and artist != "Unknown":
        return True
    else:
        return False


def get_image_pixbuf(image_data = None, width = 50, height = 50):
    assert image_data is not None
    loader = GdkPixbuf.PixbufLoader()
    loader.write(image_data)
    loader.close()
    pixbuf = loader.get_pixbuf()
    if (pixbuf.get_width() > width or pixbuf.get_height() > height):
        pixbuf = pixbuf.scale_simple(width, height, 
                                     GdkPixbuf.InterpType.BILINEAR)
    return pixbuf

