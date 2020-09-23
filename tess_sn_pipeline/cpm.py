import os

import astropy.units as u
from astropy import coordinates
from astropy.coordinates import SkyCoord
from astroquery.mast import utils
import tess_cpm

# Helper functions for doing CPM
class CPM():
    def __init__(self, ra, dec, sector, ffi_size):
        self.ra = ra
        self.dec = dec
        self.sector = sector 
        self.ffi_size = ffi_size
    
    def check_before_download(self, coordinates=None, size=5, sector=None, path=".", inflate=True, objectname=None, force_download=False):
        coords = utils.parse_input_location(coordinates, objectname)
        ra = f"{coords.ra.value:.6f}"
        matched = [m for m in os.listdir(path) if ra in m]
        if (len(matched) != 0) and (force_download == False):
            print(f"Found the following FITS files in the \"{path}/\" directory with matching RA values.")
            print(matched)
            print("If you still want to download the file, set the \'force_download\' keyword to True.")
            return matched
        else:
            path_to_FFIs = Tesscut.download_cutouts(coordinates=coordinates, size=size, sector=sector, path=path, inflate=inflate, objectname=objectname)
            print(path_to_FFIs)
            return path_to_FFIs 
        
    def FFI_source(self):
        # Check path
        PATH = self.check_before_download(coordinates=SkyCoord(self.ra, self.dec, unit="deg"), sector=self.sector, size=self.ffi_size)
        return (tess_cpm.Source(PATH[0], remove_bad=True)) # load as TESS CPM object
    

def apply_CPM(sn, r0=25, pixel_window=1):
    """
    Given a FFI tess CMP object this function will peform a detrending according to CPM. 

    Input:
    ----- 
    sn: FFI TESS CPM object
    pixel_window (float): offset we apply to the central pixel to select rows & columns
    r0 (float): center pixel of the FFI (we apply a +/- 1 offset from this pixel (i.e we select pixels row/columns (25-pixel_window, and 25+pixel_window)))
    
    Output:
    ------
    CPM Flux (currently unkown units?!) 

    """
    
    # Q: do we need to tweak these parameters for each FFI case? 

    # Find the central pixel and make a 3x3 selection
    sn.set_aperture(rowlims=[r0-pixel_window, r0+pixel_window], collims=[r0-pixel_window, r0+pixel_window])
    
    sn.add_cpm_model(exclusion_size=5, n=64, predictor_method="similar_brightness")
    sn.add_poly_model(scale=2, num_terms=4) # add polynomial detrending for longterm systematics in TESS
    
    sn.set_regs([0.01, 0.1])  # The first term is the CPM regularization while the second term is the polynomial regularization value.
    sn.holdout_fit_predict(k=50);  # When fitting with a polynomial component, we've found it's better to increase the number of sections.
    

    sn_aperture_normalized_flux = sn.get_aperture_lc(data_type="normalized_flux") # normalize flux
    sn_aperture_cpm_prediction = sn.get_aperture_lc(data_type="cpm_prediction") # CPM prediction
    sn_aperture_poly_prediction = sn.get_aperture_lc(data_type="poly_model_prediction") # polynomial prediction
    
    sn_aperture_detrended_flux = sn.get_aperture_lc(data_type="cpm_subtracted_flux") # CPM subtract

    return (sn_aperture_detrended_flux)