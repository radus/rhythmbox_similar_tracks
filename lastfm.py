from gi.repository import RB
from music_classes import SimilarArtist, SimilarTrack
from pprint import pprint
import urllib
import json
import netlib

API_KEY = "1098ad8fead1da06532f3f17b1b6be8b"
API_ROOT_URL = "http://ws.audioscrobbler.com/2.0/"

def get_similar_artists_async(artist = "", num_results = 10, 
                              success_callback = None, error_callback = None):
    url = create_request_url({'method': 'artist.getsimilar', 
                             'artist': artist, 'limit': num_results,
                             'autocorrect': 1});
    print "Getting url %s" % url
    netlib.get_url_async(url, similar_artists_cb, artist, 
                         success_callback, error_callback)


def similar_artists_cb(data, artist_queried, success_callback, error_callback):
    """
    Callback for a similar artists query. Takes the raw data returned by 
    the last.fm query and transforms it to a python dictionary. This is then
    used to run the callback function.

    Arguments:
    data - data returned by last.fm query. Should be in JSON format
    callback - function to call with the processed data. Should expect as 
    parameter a dictionary with keys:
        - artist_queried: artist for which the query was done
        - similars: list of SimilarArtists
    """
    assert success_callback is not None
    results = {}
    json_data = json.loads(data)
    json_artists_data = json_data["similarartists"]
    results["artist_queried"] = artist_queried

    results["similars"] = []
    for json_artist in json_artists_data["artist"]: 
        name = json_artist["name"]
        image_url = json_artist["image"][0]["#text"]
        similarity = float(json_artist["match"])
        new_artist = SimilarArtist({'name': name, 
                                    'image_url': image_url,
                                    'similarity': similarity})
        results["similars"].append(new_artist)
        
    success_callback(results)
    

def get_similar_tracks_async(artist = "", track = "", num_results = 10,
                             success_callback = None, error_callback = None):
    url = create_request_url({'method': 'track.getsimilar',
                              'track': track, 'artist': artist,
                              'limit': num_results, 
                              'autocorrect': 1});
    print "Getting url for similar track %s" % url
    netlib.get_url_async(url, similar_tracks_cb, track, success_callback,
                         error_callback)


def similar_tracks_cb(data, track, success_callback, error_callback):
    assert success_callback is not None
    json_data = json.loads(data)
    json_tracks = json_data["similartracks"]
    results = {}
    results["track_queried"] = track
    results["similars"] = []
    for track in json_tracks['track']:
        name = track['name']
        artist = track['artist']['name']
        image_url = track['image'][0]['#text']
        similarity = float(track['match'])
        new_similar_track = SimilarTrack({'name': name, 'artist':artist,
                                          'image_url': image_url,
                                          'similarity': similarity})
        results['similars'].append(new_similar_track)
    success_callback(results)


def create_request_url(request_params):
    request_params['api_key'] = API_KEY
    request_params['format'] = 'json'
    url = API_ROOT_URL + "/?%s" % urllib.urlencode(request_params)
    return url
     
                             
