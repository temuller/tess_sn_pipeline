from alerce.api import AlerceAPI
import pandas as pd
import matplotlib.pyplot as plt

def single_query(ra, dec, start_mjd, end_mjd):
    """ Query for a single target using the Alerce API (https://alerce.readthedocs.io/en/latest/)

    Parameters
    ----------
    ra : float
        Target's RA.
    dec : float
        Target's Dec.
    start_mjd : float
        Lower limit of the time range to query.
    end_mjd : float
        Upper limit of the time range to query.

    Returns
    -------
    DataFrame with the target's query.
    """

    params = {
    #"total": total,
    "query_parameters": {
      "coordinates":{
        "ra": ra,
        "dec": dec,
        "sr": 61200 #This is roughly 12*sqrt(2) degrees
      },
      "filters": {
        "dates": {
          "firstmjd": {
            "min": start_mjd - 30,
            "max": end_mjd
          }
        }
      }
    }
    }
    api = AlerceAPI()
    resp_df = api.query(params, format="pandas")
    
    return resp_df

def get_queries(pointings_df):
    """ Multiple queries for the different sectors and cameras.

    Parameters
    ----------
    pointings_df : DataFrame
        DataFrame with TESS pointings information (obtained with `get_sector_pointings`).

    Returns
    -------
    A list of queries for each Camera in a dictionary with the Cameras as key values.
    """

    resp_dict = {}
    for i in np.arange(1, 5):
        ra_list, dec_list = pointings_df[f'RA{i}'], pointings_df[f'Dec{i}']
        start_mjd_list, end_mjd_list = pointings_df['StartMJD'], pointings_df['EndMJD']
      
        resp_list = list(map(single_query, ra_list, dec_list, start_mjd_list, end_mjd_list))
        resp_dict[f'Camera{i}'] = resp_list

    return resp_dict

def plot_ztf_target(name):
    """ Given a ZTF target, this will plot a ZTF light curve from Alerce.
    
    E.g., ZTF18acpfwmm

    Parameters
    ----------
    name : str
        ZTF target name.
        
    """

    api = AlerceAPI()
    resp = api.get_detections(name, format="pandas")

    times = resp.mjd.values
    mags = resp.magap.values
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    ax.errorbar(times, mags, 0.0, fmt='o', ms=10)
    
    ax.set_xlabel('MJD', fontsize=14)
    ax.set_ylabel('Apparent Mag.', fontsize=14)
    ax.set_title(name, fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.gca().invert_yaxis()
    plt.show()