import numpy as np
import paths

##############################################################################
####################   Constants    ##########################################
##############################################################################


npixs = {"IGRINS": 1848, "CRIRES": 1024}
nks = {"IGRINS": 125, "CRIRES": 203}

goodchipslist = {
    "IGRINS": {
        "W1049B":{
            "K": [0, 1, 2, 3, 4, 5, 15, 16, 17, 18], #[1, 4, 13], #
            "H": [0, 1, 2, 3, 4, 5, 16, 17, 18, 19] 
        },
        "W1049A":{
            "K": [0, 1, 2, 3, 4, 5, 15, 16, 17, 18], 
            "H": [0, 1, 2, 3, 4, 5, 16, 17, 18, 19]
        },
        "W1049B_0209":{
            "K": [2, 3, 4, 5, 15, 16, 17, 18], # snr 20-30: 6, 7, 8, 13, 14, 15, 19
            "H": [0, 1, 2, 3, 4, 5, 16, 17, 18, 19] 
        },
        "W1049A_0209":{
            "K": [0, 1, 2, 3, 4, 5, 6, 7, 13, 14, 15, 16, 17], 
            "H": [ 2,  3,  4,  5, 16, 17, 18, 19]
        },
        "2M0036_1103":{
            "K": [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19], # [2,3,4,5,8,10,11,12,13,14,15,18], 
            "H": [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]#[0, 1, 2, 3, 4, 5, 6, 15, 16, 17, 18, 19]
        },
        "2M0036_1105":{
            "K": [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19], #[2,3,4,5,8,10,11,12,13,14,15,18], 
            "H": [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]#[1,2,3,4,5,9,10,11,16], #[0, 1, 2, 3, 4, 5, 6, 15, 16, 17, 18, 19]
        },      
    }, # [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19],
    "CRIRES": {
        "W1049B":{
            "K": [0, 1, 2, 3]
        },
        "W1049A":{
            "K": [0, 1, 2, 3]
        }
    }
}

bestmodels = {
    "W1049B": {"K":"t1500g1000f8",
               "H":"t1400g1000f8"},
    "W1049A": {"K":"t1500g1000f8",
               "H":"t1500g1000f8"},
    "W1049B_0209": {"K":"t1500g1000f8",
                    "H":"t1400g1000f8"},
    "W1049A_0209": {"K":"t1500g1000f8",
                    "H":"t1500g1000f8"},
    "2M0036_1103": {"K":"t1500g1000f8",
                    "H":"t1500g1000f8"},
    "2M0036_1105": {"K":"t1500g1000f8",
                    "H":"t1500g1000f8"}
}

nobss =   {"W1049B": 14,     "W1049A": 14,     "W1049B_0209": 14,     "W1049A_0209": 14,     "2M0036_1103": 7   ,  "2M0036_1105": 8}
periods = {"W1049B": 5,      "W1049A": 7,      "W1049B_0209": 5,      "W1049A_0209": 7,      "2M0036_1103": 2.7 ,  "2M0036_1105": 2.7}
incs =    {"W1049B": 80,     "W1049A": 70,     "W1049B_0209": 80,     "W1049A_0209": 70,     "2M0036_1103": 51  ,  "2M0036_1105": 51}
vsinis =  {"W1049B": 29,     "W1049A": 21,     "W1049B_0209": 29,     "W1049A_0209": 21,     "2M0036_1103": 33,    "2M0036_1105": 33} # km/s
rvs =     {"W1049B": 7.05e-5,"W1049A": 5.4e-5, "W1049B_0209": 7.05e-5,"W1049A_0209": 5.4e-5, "2M0036_1103": 6.5e-5,"2M0036_1105": 6.5e-5} # rv in km/s / c in km/s
                #9e-5 9.3e-5if CRIRES 7.4e-5 5.4e-5 if IGRINS

timestamps = { # obs times in hour, computed from obs headers (JD-DATE)
    "W1049B": np.array(
        [0.134892  , 0.49418401, 0.85395001, 1.213902  , 1.5732    ,
        1.93294201, 2.30937601, 2.66913001, 3.19404001, 3.61374   ,
        3.987222  , 4.35165001, 4.71316801, 5.07270601]), 
    "W1049A": np.array(
        [0.134892  , 0.49418401, 0.85395001, 1.213902  , 1.5732    ,
        1.93294201, 2.30937601, 2.66913001, 3.19404001, 3.61374   ,
        3.987222  , 4.35165001, 4.71316801, 5.07270601]),
    "W1049B_0209": np.array(
        [0.15093   , 0.51746401, 0.87756001, 1.23739201, 1.59770401,
        1.97218201, 2.341842  , 2.70773401, 3.07090801, 3.435258  ,
        3.80697001, 4.168056  , 4.52813401, 4.88789401]),
    "W1049A_0209": np.array(
        [0.15093   , 0.51746401, 0.87756001, 1.23739201, 1.59770401,
        1.97218201, 2.341842  , 2.70773401, 3.07090801, 3.435258  ,
        3.80697001, 4.168056  , 4.52813401, 4.88789401]),
    "2M0036_1103": np.array(
        [0.        , 0.35493599, 0.709224  , 1.063536  , 2.07012   ,
        2.424528  , 2.779728  ]),
    "2M0036_1105": np.array(
        [0.        , 0.35536801, 0.727008  , 1.08223201, 1.43724001,
       1.79220001, 2.14716   , 2.50233601]),
}


##############################################################################
####################    Settings    ##########################################
##############################################################################


#################### Run settings ####################################

use_eqarea = True


########## IC14 parameters ##########
lld = 0.4
alpha = 2000
ftol = 0.01 # tolerance for convergence of maximum-entropy
nstep = 2000
nlat, nlon = 10, 20

########## Starry parameters ##########
ydeg_sim = 16
ydeg = 8
udeg = 1
nc = 1
vsini_max = 40000.0

########## Starry optimization parameters ##########
lr_LSD = 0.001
niter_LSD = 5000
lr = 0.01
niter = 5000

#################### Automatic ####################################

def load_config(instru, target, band, sim=False):
    # Auto consistent options

    nobs = nobss[target]
    nk = nks[instru]

    # set chips to include
    goodchips = goodchipslist[instru][target][band]
    modelspec = bestmodels[target][band]

    # set model files to use
    rv = rvs[target]
    if instru == "CRIRES":
        rv = 9e-5

    # set solver parameters
    period = periods[target]
    inc = incs[target]
    vsini = vsinis[target]
    veq = vsini / np.sin(inc * np.pi / 180)

    # set time and period parameters
    timestamp = timestamps[target]
    phases = timestamp * 2 * np.pi / period # 0 ~ 2*pi in rad
    theta = 360.0 * timestamp / period      # 0 ~ 360 in degree

    params_starry = dict(
        ydeg=ydeg_sim,
        udeg=udeg,
        nc=nc,
        veq=veq*1e3,
        inc=inc,
        nt=nobs,
        vsini_max=vsini_max,
        u1=lld,
        theta=theta)

    params_run = dict(
        nk=nk,
        phases=phases,
        timestamps=timestamp,
        inc=inc, 
        vsini=vsini,
        rv=rv,
        lld=lld, 
        eqarea=use_eqarea, 
        nlat=nlat, 
        nlon=nlon,
        alpha=alpha
    )

    if sim:
        return params_starry, params_run, goodchips, modelspec
    else:
        return params_run, goodchips, modelspec