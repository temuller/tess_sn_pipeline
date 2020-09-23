import numpy as np
import request

import astropy.units as u
from astropy import coordinates
from astropy.time import Time

def date_to_mjd(date):
    """ Converts a TESS date to mjd.

    Parameters
    ----------
    date : str
        Date of TESS pointings.

    Returns
    -------
    Modified Julian Date (float).
    """
    
    month, day, year = date.split('/')
    isot = f'20{year}-{month}-{day}T00:30:00'
    mjd = np.round(Time(isot).mjd, 3)
    
    return mjd

def get_cam_coords(tess_cam_coords):
    """ Extract RA and Dec for a given TESS camera.

    Parameters
    ----------
    tess_cam_coords : str
        TESS camera coordnates

    Returns
    -------
    A list of RA and a list of Dec.
    """

    ra_list, dec_list = [], []
    for coords in tess_cam_coords:
        ra, dec, _ = coords.split(',')
        ra_list.append(ra), dec_list.append(dec)
      
    return ra_list, dec_list

def get_osc_coords(object_name):
    """ Get object coordinates from the Open Supernova Catalog (OSC).

    Parameters
    ----------
    object_name : str
        Object's name to search on OSC.

    Returns
    -------
    Astropy SkyCoord with the object's coordinates and `maxdate` value (in MJD) 
    of the object from OSC.
    """
    
    # get object metadata
    osc_link = f'https://astrocats.space/api/{object_name}/ra+dec+maxdate'
    osc_request = requests.get(osc_link).json()
    osc_data    = osc_request[object_name]
    
    # get coordinates
    ra = osc_data['ra'][0]['value']
    dec = osc_data['dec'][0]['value']
    maxdate = osc_data['maxdate'][0]['value']
    maxmjd = Time(maxdate.replace('/','-')+'T00:00:00', format='isot', scale='utc').mjd
    
    coords = coordinates.SkyCoord(ra, dec, unit=(u.hourangle, u.deg))
    return coords, maxmjd