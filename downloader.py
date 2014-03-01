"""A basic module designed to download images on your server.
Please note this is always a risky thing to do.
I've added a pretty basic safety that will check what we downloaded
is REALLY an image, however this could prove not to be enough,
so use with caution."""

import urllib2
import os
from PIL import Image

def download(path, url, count):
    """Given a path (basis), a url, and a number, will :
    - Compute a destination name for the image, based on the number transformed to an hex (because hex are cool).
    - Try and download an image from the URL, and save it to the server in the static folder of the Falsk app,
    with the new, computed name.
    - Return this new name so it can be saved - without the path - in a database."""
    hex_name = next_as_hexa(count) + '.' + url.split(".")[-1]
    new_name = path + hex_name
    download_url_to(url, new_name)
    return hex_name

def download_url_to(url, filename):
    """Download a file, byte from byte, from a given URL and check it is an image.
    If it is not an image, remove the image and throw an IOError."""
    u = urllib2.urlopen(url)
    f = open(filename, 'wb')
    meta = u.info()
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        f.write(buffer)
    f.close()
    if not check_if_image(filename):
        # Not an image : let's delete this, better safe than sorry
        os.remove(filename)
        raise IOError("This is not an image !")

def check_if_image(filename):
    """Check if it is animage by using PIL. If PIL cannot open the file,
    it is not an image."""
    try:
        Image.open(filename)
    except IOError:
        return False
    return True

def size_of_folder(basis):
    """Compute the size of the static img repo."""
    return bytes_as_megabytes(sum([os.path.getsize(basis + "static/img/" + f) for f in os.listdir(basis + "static/img")]))

def bytes_as_megabytes(num):
    """Simply convert bytes to MB for human readability. Should be improved to handle GB."""
    return str(num//(1000*1000)) + "MB"

def next_as_hexa(num):
    return hex(num + 1)
