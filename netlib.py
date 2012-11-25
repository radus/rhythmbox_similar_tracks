import rb

def get_url_async(url, callback, *args):
    loader = rb.Loader()
    loader.get_url(url, callback, *args)
