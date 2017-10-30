import sys
import os
sys.path.insert(1,'python')
sys.path.insert(1,'/soft/python/lib64/python2.7/site-packages')
import numpy as np 
import math
from astropy.io import fits
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.constants
from mcmc_routines import *
from plotting_fns import remove_ticks
from matplotlib.gridspec import GridSpec
import matplotlib.ticker as ticker
import emcee
import corner
import joblib
from joblib import Parallel, delayed

def SEDfit(x,x_smooth,y,yerr,snr,z,Lx,init,snr_lim,i,field):
	if np.sum(snr)<=snr_lim:
		return

	ydat = y
	ydat = np.nan_to_num(ydat)

	ydaterr = yerr
	ydaterr = np.nan_to_num(ydaterr)

	xdat = x/(z+1)

	all_T    = []
	all_Ngb  = []
	all_Ny   = []
	all_alp  = []
	all_Lir  = []
	all_turn = []

	nwalkers=200
	ndim=5
	nsteps = 600
	burnin = 300

	length = nwalkers*(nsteps-burnin)

	lum = np.zeros((length))
	lum.fill(Lx)
	lum = [lum]
	redshift = np.zeros((length))
	redshift.fill(z)
	redshift = [redshift]

	pos=initpos(init,0.002,nwalkers)
	sampler = emcee.EnsembleSampler(nwalkers, ndim, lnpost,
	                                args=(xdat,ydat,ydaterr))

	output=sampler.run_mcmc(pos, nsteps)

	samples=sampler.chain[:, burnin:, :].reshape((-1, ndim)).transpose()

	all_T.append(samples[0])
	all_Ny.append(samples[1])
	all_Ngb.append(samples[2])
	all_alp.append(samples[3])
	all_turn.append(samples[4])

	################
	# # Plot walkers
	################
	# f,(ax1,ax2,ax3,ax4)=plt.subplots(4,sharex=True)
	# ax1.plot(sampler.chain[:,:,0].transpose(),color='black',alpha=0.5)
	# ax2.plot(sampler.chain[:,:,1].transpose(),color='black',alpha=0.5)
	# ax3.plot(sampler.chain[:,:,2].transpose(),color='black',alpha=0.5)
	# ax4.plot(sampler.chain[:,:,3].transpose(),color='black',alpha=0.5)
	# plt.show()
	# fig = corner.corner(samples.transpose(),labels=('T','Ny','Ngb','alpha'))
	# plt.show()

	##############
	# Calculate functions, likelihoods and IR luminosities for each of the samples
	##############
	fns=[]
	gbs=[]
	pls=[]
	likes=[]
	for p in np.arange(0,length,10):
		fn,gb,pl,turn = model_plus(x_smooth,samples[0][p],samples[1][p],samples[2][p],samples[3][p],samples[4][p])
		like = lnlike((samples[0][p],samples[1][p],samples[2][p],samples[3][p],samples[4][p]),xdat,ydat,ydaterr)
		# plt.plot(x_smooth, fn, color=colours[4],alpha=0.1)
		fns.append(fn)
		gbs.append(gb)
		pls.append(pl)
		likes.append((-2*like)/5)
		L = int_gb(x_smooth,samples[0][p],samples[1][p],samples[2][p],samples[3][p],z)[0]
		all_Lir.append(L.value)
	all_Lir = [np.array(all_Lir)]
	likes = [np.array(likes)]
	# plt.hist(likes,bins=50,histtype='step',fill=True,color='gray',facecolor='gray',lw='2',normed='True',alpha=0.8)
	# plt.show()
	likes = np.array(likes)
	best = (np.abs(likes-1)).argmin()
	# val = likes[best]																																																																																																																																																																																																																																																															

	curve_best=fns[best]

	gb_best = gbs[best]
	pl_best = pls[best]
	# gb_best = model_plus(x_smooth, samples[0][best], samples[1][best],samples[2][best],samples[3][best],samples[4][best])[1]
	# pl_best = model_plus(x_smooth,samples[0][best], samples[1][best],samples[2][best],samples[3][best],samples[4][best])[2]
	curve_up,curve_lo = np.percentile(fns,(84,16),axis=0)

	################
	# Calculate percentiles from parameter distributions 
	###############
	T_upper,T_lower,T_mid             = np.percentile(samples[0],(84,16,50), axis=0)
	N_y_upper,N_y_lower,N_y_mid       = np.percentile(samples[1],(84,16,50), axis=0)
	N_gb_upper,N_gb_lower,N_gb_mid    = np.percentile(samples[2],(84,16,50), axis=0)
	alpha_upper,alpha_lower,alpha_mid = np.percentile(samples[3],(16,84,50), axis=0)
	turn_upper,turn_lower,turn_mid    = np.percentile(samples[4],(16,84,50), axis=0)

	##############
	# Plot data and fits 
	##############
	a7 = plt.subplot()
	a7.scatter(xdat,ydat,c='gray',edgecolor='none')
	a7.errorbar(xdat,ydat,yerr=ydaterr,linestyle='none',c='gray')
	both = model_plus(x_smooth,T_mid,N_y_mid,N_gb_mid,alpha_mid,turn_mid)[0]
	gb = model_plus(x_smooth,T_mid,N_y_mid,N_gb_mid,alpha_mid,turn_mid)[1]
	pl = model_plus(x_smooth,T_mid,N_y_mid,N_gb_mid,alpha_mid,turn_mid)[2]	
	# a7.plot(x_smooth,both,c='black',linestyle='-',alpha=0.7,label='fit')
	# a7.plot(x_smooth,gb,c='black',linestyle='--',label='greybody')
	# a7.plot(x_smooth,pl,c='black',linestyle='--',label='MIR')	
	a7.plot(x_smooth,curve_best,c='darkblue',linestyle='-',alpha=0.7,label='fit')
	a7.plot(x_smooth,gb_best,c='gray',linestyle='--',label='greybody')
	a7.plot(x_smooth,pl_best,c=colours[4],linestyle='--',label='MIR')
	a7.fill_between(x_smooth,curve_up,curve_lo,facecolor=colours[4],alpha=0.5,label='_nolegend_',lw=0)
	a7.invert_xaxis()
	a7.set_xscale('log')
	a7.set_yscale('log')
	a7.set_ylim(1e-3,1e-1)		
	a7.set_xlim(1e-3,1e-5)
	a7.text(0.8,0.9, "MCMC", va="center", ha="center", transform=a7.transAxes)
	a7.set_xticks([1000e-6,100e-6,10e-6])
	a7.xaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=None))
	a7.set_xticklabels(["1000","100","10"])
	a7.set_yticks([10e-3,1e-3,0.1e-3])
	a7.yaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=None))
	a7.set_yticklabels(["10","1","0.1"])
	a7.tick_params(axis='x',which='both',top='off')	
	a7.tick_params(axis='y',which='both',right='off')
	a7.set_xlabel("Rest frame wavelength (micron)")
	a7.set_ylabel("Flux (mJy)",labelpad=-10)
	# a7.legend()

	# plt.show()
	plt.savefig('/home/joanna/results/2017_10/imgs/image_test_{:04d}.png'.format(i))
	plt.close()


	# data = (np.array([all_T,all_Ny,all_Ngb,all_alp,all_turn,lum,redshift,likes,all_Lir]).T)
	# with open('/car-data/joanna/data/fields/{}/SED_output/SED_out_{:04d}'.format(field,i),'a') as f_handle:
	#     np.save(f_handle, data)
#######################################################################################################################

colours = ["#FF0000", "#00A08A", "#F2AD00", "#F98400", "#5BBCD6","#FF0000", "#00A08A"]

#################
# Initialise variables
#################
B    = 1.5
T    = 20
N_y  = 0.03
N_gb = 0.03
alpha  = 2
turn = 25

init = [T,N_y,N_gb,alpha,turn]
x_smooth = np.arange(1e-7,1e-2,0.1e-6)
snr_lim = 100

n_jobs = 32

#################
#################
# COSMOS
#################

# os.chdir('/car-data/joanna/data/fields/COSMOS')
os.chdir('/data/joanna/data/fields/COSMOS')

fluxes = fits.open('fluxes_S2_MIPS_PEP_SPIRE_new.fits')[1].data
# fluxes = np.sort(fluxes,order='Lx')
# fluxes = fluxes[fluxes['Lx']>10**45.125]

y = np.array([fluxes['f24'],fluxes['f70'],fluxes['f100'],fluxes['f160P'],fluxes['f250'],fluxes['f350'],fluxes['f500'],fluxes['f850']]).T
yerr = np.array([fluxes['f24err'],fluxes['f70err'],fluxes['f100err'],fluxes['f160Perr'],fluxes['f250err'],fluxes['f350err'],fluxes['f500err'],fluxes['f850err']]).T
snr = y/yerr
x = np.array([24,70,100,160,250,350,500,850])*1e-6
z = fluxes['z']
Lx = fluxes['Lx']

for i in range(len(y)):
	SEDfit(x,x_smooth,y[i],yerr[i],snr[i],z[i],Lx[i],init,snr_lim,i,'COSMOS')

# Parallel(n_jobs=n_jobs)(delayed(SEDfit)(x,x_smooth,y[i],yerr[i],snr[i],z[i],Lx[i],init,snr_lim,i,'COSMOS') for i in range(len(y)))

#################
# EGS
################## 
# os.chdir('/car-data/joanna/data/fields/EGS')
# os.chdir('/data/joanna/data/fields/EGS')

fluxes = fits.open('fluxes_S2_MIPS_PEP_SPIRE_new.fits')[1].data
# fluxes = np.sort(fluxes,order='Lx')
# fluxes = fluxes[fluxes['Lx']>10**45.125]

y = np.array([fluxes['f24'],fluxes['f70'],fluxes['f100'],fluxes['f160P'],fluxes['f250'],fluxes['f350'],fluxes['f500'],fluxes['f850']]).T
yerr = np.array([fluxes['f24err'],fluxes['f70err'],fluxes['f100err'],fluxes['f160Perr'],fluxes['f250err'],fluxes['f350err'],fluxes['f500err'],fluxes['f850err']]).T
snr = y/yerr
x = np.array([24,70,100,160,250,350,500,850])*1e-6
z = fluxes['z']
Lx = fluxes['Lx']

# for i in range(len(y)):
# 	SEDfit(x,x_smooth,y[i],yerr[i],snr[i],z[i],Lx[i],init,snr_lim,i,'EGS')

# Parallel(n_jobs=n_jobs)(delayed(SEDfit)(x,x_smooth,y[i],yerr[i],snr[i],z[i],Lx[i],init,snr_lim,i,'EGS') for i in range(len(y)))

#################
# CDFS
################## 
os.chdir('/car-data/joanna/data/fields/CDFS')
# os.chdir('/data/joanna/data/fields/CDFS')

fluxes = fits.open('fluxes_S2_MIPS_PEP_SPIRE_new.fits')[1].data
# fluxes = np.sort(fluxes,order='Lx')
# fluxes = fluxes[fluxes['Lx']>10**45.125]

fluxes['f870']=fluxes['f870']*1000
fluxes['f870err']=fluxes['f870err']*1000
fluxes = fluxes[fluxes['f870']>0.0]
y = np.array([fluxes['f24'],fluxes['f70'],fluxes['f100'],fluxes['f160P'],fluxes['f250'],fluxes['f350'],fluxes['f500'],fluxes['f870']]).T
yerr = np.array([fluxes['f24err'],fluxes['f70err'],fluxes['f100err'],fluxes['f160Perr'],fluxes['f250err'],fluxes['f350err'],fluxes['f500err'],fluxes['f870err']]).T
snr = y/yerr
x = np.array([24,70,100,160,250,350,500,870])*1e-6
z = fluxes['z']
Lx = fluxes['Lx']

# for i in range(len(y)):
# 	SEDfit(x,x_smooth,y[i],yerr[i],snr[i],z[i],Lx[i],init,snr_lim,i,'CDFS')

# Parallel(n_jobs=n_jobs)(delayed(SEDfit)(x,x_smooth,y[i],yerr[i],snr[i],z[i],Lx[i],init,snr_lim,i,'CDFS') for i in range(len(y)))
