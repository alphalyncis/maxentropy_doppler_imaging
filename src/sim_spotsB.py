import numpy as np
import paths
import os

from dime import DopplerImaging, load_data_from_pickle, make_fakemap, simulate_data
from config import load_config

instru = "IGRINS"
target = "W1049B"
band = "K"
params_starry, params_run, goodchips, modelspec = load_config(instru, target, band, sim=True)
model_datafile = paths.data / f"fitted/{instru}_{target}_{band}_{modelspec}.pickle"
contrast = 0.8
#goodchips = [1,2,3,4]

for maptype in ["1spot", "2spot"]:
    savedir = f"sim_B_{maptype}"

    if not os.path.exists(paths.figures / savedir):
        os.makedirs(paths.figures / savedir)

    ##############################################################################
    ####################      Sim!      ##########################################
    ##############################################################################

    # Load data from fit pickle
    wav_nm, template, _, error = load_data_from_pickle(model_datafile, goodchips)
    flux_err = eval(f'{np.median(error):.3f}')

    # Make mock observed spectra
    lat_deg = 30 if maptype == "1spot" else 0
    
    fakemap = make_fakemap(maptype, contrast, 
        r_deg=30, lat_deg=lat_deg, lon_deg=90, 
        r1_deg=25, lat1_deg=45, lon1_deg=-60)

    mean_spectrum = np.median(template, axis=0)
    observed = simulate_data(fakemap, mean_spectrum, wav_nm, flux_err, params_starry, 
                            plot_ts=True, custom_plot=False,
                            savedir=paths.figures/f"{savedir}/fakemap.png")

    map_sim = DopplerImaging(wav_nm, goodchips, params_run)
    map_sim.load_data(observed, template, error)
    map_sim.make_lsd_profile(modelspec, plot_lsd_profiles=True, plot_deviation_map=True, savedir=paths.figures/f"{savedir}")
    map_sim.solve(create_obs_from_diff=True, solver='scipy')
    map_sim.plot_mollweide_map(vmin=85, vmax=110, savedir=paths.figures/f"{savedir}/solver1.png")