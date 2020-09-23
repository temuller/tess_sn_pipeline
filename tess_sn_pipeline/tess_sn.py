import numpy as np
import pandas as pd

def get_sector_pointings(years=[1, 2, 3]):
    """ Retrieves TESS pointings for the sectors in the given years.

    Parameters
    ----------
    years : array-like
        Years of TESS pointings.

    Returns
    -------
    DataFrame with TESS pointings information.
    """
    
    base_url = 'https://raw.githubusercontent.com/villrv/tess_data/master/'
    columns = ['Sector', 'Dates', 'Spacecraft', 'Camera1', 'Camera2',	'Camera3', 'Camera4']
    
    # get data from the base_url
    pointings_df = pd.DataFrame(columns=columns)
    for i in years:
        url = os.path.join(base_url, f'year{i}.dat')
        year_df = pd.read_csv(url, names=columns, delim_whitespace=True, skiprows=1)
        pointings_df = pd.concat([pointings_df, year_df], ignore_index=True)
        
    # add starting and ending mjd for each sector
    start_mjd_col, end_mjd_col = [], []
    for pointing_dates in pointings_df.Dates:
        start_mjd, end_mjd = list(map(date_to_mjd, pointing_dates.split('-')))
        start_mjd_col.append(start_mjd), end_mjd_col.append(end_mjd)
        
    pointings_df['StartMJD'], pointings_df['EndMJD'] = start_mjd_col, end_mjd_col
    
    # extract RA and Dec for each camera
    for i in np.arange(1, 5):
        cam = f'Camera{i}'
        ra_list, dec_list = get_cam_coords(pointings_df[cam])
        
        pointings_df[f'RA{i}'], pointings_df[f'Dec{i}'] = ra_list, dec_list
        
    return pointings_df

def tess_observed(sector, time, pointings_df):
    """ Check if a SN should be visible in a given TESS sector.

    Parameters
    ----------
    sector : int
        TESS sector number.
    time : float
        Time at which to check if the SN was observed by TESS.
    pointings_df : DataFrame
        DataFrame with TESS pointings information (obtained with `get_sector_pointings`).

    Returns
    -------
    Bool. True if TESS observed the SN in the given time window, False otherwise.
    """
    
    sector_df = pointings_df[pointings_df.Sector==sector]
    start_mjd, end_mjd = sector_df.StartMJD.values[0], sector_df.EndMJD.values[0]

    if (time > start_mjd - 30) and (time < end_mjd + 100):
        print(f'This transient is in sector {sector}')
        return True
    
    print(f'This transient is NOT in sector {sector}')
    return False