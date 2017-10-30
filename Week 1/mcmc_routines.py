import emcee
import numpy as np
import matplotlib.pyplot as plt
import scipy.constants
import scipy.integrate as integrate
from astropy.cosmology import WMAP9 as cosmo
import astropy.units as u

def model(x,T,N_y,N_gb,alpha,turn):
    h = scipy.constants.h
    k = scipy.constants.k
    c = scipy.constants.c
    B = 1.5
    factor=2*h/c**2
    turnover = turn
    gb = ((c/x)**(3+B))/(np.exp((h*c)/(x*k*T))-1)
    gb = N_gb*(gb/np.amax(gb))   # normalise
    pl = (x**alpha)*(np.exp(-x/(turnover*1e-6))**2)
    pl = N_y*(pl/np.amax(pl))   # normalise
    return(gb+pl)

def model_plus(x,T,N_y,N_gb,alpha,turn):
    h = scipy.constants.h
    k = scipy.constants.k
    c = scipy.constants.c
    B = 1.5
    factor=2*h/c**2
    turnover=turn
    gb = ((c/x)**(3+B))/(np.exp((h*c)/(x*k*T))-1)
    gb = N_gb*(gb/np.amax(gb))   # normalise
    pl = (x**alpha)*(np.exp(-x/(turnover*1e-6)))**2
    pl = N_y*(pl/np.amax(pl))   # normalise
    return(gb+pl,gb,pl,turnover)

def gb_model(x,T,N_y,N_gb,alpha):
    h = scipy.constants.h
    k = scipy.constants.k
    c = scipy.constants.c
    B = 1.5
    factor=2*h/c**2
    gb = factor*((c/x)**(3+B))/(np.exp((h*c)/(x*k*T))-1)
    gb = N_gb*(gb/np.amax(gb))   # normalise
    gb = gb*1e-23
    return(gb)

def lnlike(X,x,y,yerr):
    """
    Return the log-likelihood (-0.5 * chi^2) for a state vector X
    given the data x,y,yerr
    """
    T,N_y,N_gb,alpha,turn=X
    return -0.5*np.nansum((y - model(x,T,N_y,N_gb,alpha,turn))**2 / yerr**2)

def lnprior(X):
    """
    Return the log prior on the state vector X. Used here to specify
    the rectangular bounds of the allowed parameter space.
    """
    T,N_y,N_gb,alpha,turn=X
    if 10< T< 50 and 0< N_y <0.06 and 0<N_gb<0.06 and 0<alpha<10 and 10<turn<50:
    # if 0 < m < 4 and -10<c<10.0:
        return 0.0
        # return -np.log(N_y)
    return -np.inf
    
def lnpost(X,x,y,yerr):
    """
    The posterior for state vector X is the product of the prior and
    the likelihood.
    """
    return lnprior(X)+lnlike(X,x,y,yerr)

def initpos(p,s,nwalkers):
    """
    Set up the initial positions for the walkers.
    p contains an array with the reference position
    s is the Gaussian sigma to scatter around (in both dimensions)
    nwalkers is the number of walkers we plan to use
    """
    return [p+s*np.random.normal(size=len(p)) 
         for i in range(nwalkers)]

def int_gb(x,T,N_y,N_gb,alpha,z):
    pi=scipy.constants.pi
    d_l = cosmo.luminosity_distance(z)
    d_l =  d_l.to(u.m)
    L_ir = 4*pi*(d_l**2)*integrate.quad(gb_model,8e-6,1000e-6,args=(T,N_y,N_gb,alpha))
    # Unit conversion: from Jy Hz m^2, to W, to erg/s:
    L_ir = L_ir*1e26*1e-7
    return L_ir
