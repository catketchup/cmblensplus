# A quick demonstration of inpainting

import numpy as np
import healpy as hp
import basic
import curvedsky
from matplotlib.pyplot import *

# define parameters
Tcmb  = 2.726e6 # CMB temperature
lmax  = 700     # maximum multipole of alm
nside = 512
npix  = 12*nside**2
sigma = 100.    # uK'
L = np.linspace(0,lmax,lmax+1)

# load cl
cl = basic.aps.read_cambcls('../data/lensedcls.dat',2,lmax,4,bb=True)/Tcmb**2

# load mask
mask = hp.fitsfunc.read_map('../data/wmap_temperature_kq85_analysis_mask_r9_9yr_v5.fits')
#hp.mollview(mask)
#show()
mask = hp.pixelfunc.ud_grade(mask,nside)
w2 = np.average(mask**2)
print(w2)

# Gaussian alms are generated here
Talm = curvedsky.utils.gauss1alm(lmax,cl[0,:])
Tmap = mask * curvedsky.utils.hp_alm2map(npix,lmax,lmax,Talm)
Talm = curvedsky.utils.hp_map2alm(nside,lmax,lmax,Tmap)

xl0  = curvedsky.utils.alm2cl(lmax,Talm)/w2

# noise covariance
nij = mask * (sigma*(np.pi/10800.)/Tcmb)**(-2)
#nij = np.ones(npix)

# Wiener filtering
#xlm = curvedsky.cninv.cnfilter(npix,lmax,np.ones(lmax+1),nij,Talm,1000)
xlm = curvedsky.cninv.cnfilter(npix,lmax,cl[0,:],nij,Talm,1000,filter='W')
#xlm = curvedsky.cninv.cnfilter0(npix,lmax,cl[0,:],nij,Talm,100)

# power spectrum
xl1 = curvedsky.utils.alm2cl(lmax,xlm)/w2

# filtered map
#xmap = curvedsky.utils.hp_alm2map(npix,lmax,lmax,xlm)
#hp.mollview(xmap)
#hp.mollview(xmap-Tmap)
#show()
np.savetxt('cl.dat',np.array((L,cl[0,:],xl0,xl1)).T)
