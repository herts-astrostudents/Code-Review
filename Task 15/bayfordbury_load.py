import numpy as np
from astropy.io import fits


urlbase = 'https://observatory.herts.ac.uk/automation/getfit.php?id='


def download_image(obj):
    '''
    Downloads a file from the Bayfordbury server.
    https://observatory.herts.ac.uk/

    obj: tuple with two strings like (<name>, <id>), where <id> is an ID in Bayfordbury database.

    returns a tuple (<object name>, 2D image)
    '''
    f = fits.open(urlbase + obj["id"], ignore_missing_end=True)
    return (obj["name"], f[0].data)


def download_all(list_path):
    '''
    Downloads all files from the Bayfordbury server.
    https://observatory.herts.ac.uk/

    list_path: path to a file with two columns ["name","id"], id is Bayfordbury database ID.

    returns a list of tuples [(<object name>, 2D image), ...]
    '''
    objects = np.genfromtxt(list_path, dtype=["U10", "U10"], names=True)
    return [download_image(obj) for obj in objects]