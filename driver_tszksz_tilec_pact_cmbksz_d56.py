import universe
reload(universe)
from universe import *

import mass_conversion
reload(mass_conversion)
from mass_conversion import *

import catalog
reload(catalog)
from catalog import *

import thumbstack
reload(thumbstack)
from thumbstack import *

import cmb
reload(cmb)
from cmb import *

# running on cori
# 68 cores per knl node, 32 cores per haswell node
#salloc -N 1 --qos=interactive -C haswell -t 04:00:00 -L SCRATCH

##################################################################################

nProc = 32 # 1 haswell node on cori

##################################################################################
##################################################################################
# cosmological parameters

u = UnivMariana()

###################################################################################
# M*-Mh relation

massConversion = MassConversionKravtsov14()
#massConversion.plot()

###################################################################################
###################################################################################
# Galaxy catalogs

###################################################################################
# Mariana

# CMASS
cmassSMariana = Catalog(u, massConversion, name="cmass_s_mariana", nameLong="CMASS S M", pathInCatalog="../../data/CMASS_DR12_mariana_20160200/output/cmass_dr12_S_mariana.txt", save=False)
#cmassSMariana.plotHistograms()
#cmassSMariana.plotFootprint()
#cmassMariana.printProperties()
#
#cmassNMariana = Catalog(u, massConversion, name="cmass_n_mariana", nameLong="CMASS N M", pathInCatalog="../../data/CMASS_DR12_mariana_20160200/output/cmass_dr12_N_mariana.txt", save=False)
#cmassNMariana.plotHistograms()
#cmassNMariana.plotFootprint()
#cmassMariana.printProperties()
#
# combined catalog
cmassMariana = cmassSMariana.copy(name="cmass_mariana", nameLong="CMASS M")
#cmassMariana.addCatalog(cmassNMariana, save=False)
#cmassMariana.plotHistograms()
#cmassMariana.plotFootprint()
#cmassMariana.printProperties()


###################################################################################
# Kendrick

# CMASS
cmassSKendrick = Catalog(u, massConversion, name="cmass_s_kendrick", nameLong="CMASS S K", pathInCatalog="../../data/BOSS_DR10_kendrick_20150407/output/cmass_dr10_S_kendrick.txt", save=False)
#cmassSKendrick.plotHistograms()
#cmassSKendrick.plotFootprint()
#
#cmassNKendrick = Catalog(u, massConversion, name="cmass_n_kendrick", nameLong="CMASS N K", pathInCatalog="../../data/BOSS_DR10_kendrick_20150407/output/cmass_dr10_N_kendrick.txt", save=False)
#cmassNKendrick.plotHistograms()
#cmassNKendrick.plotFootprint()
#
# combined catalog
cmassKendrick = cmassSKendrick.copy(name="cmass_kendrick", nameLong="CMASS K")
#cmassKendrick.addCatalog(cmassNKendrick, save=False)
#cmassKendrick.plotHistograms()
#cmassKendrick.plotFootprint()

# LOWZ
lowzSKendrick = Catalog(u, massConversion, name="lowz_s_kendrick", nameLong="LOWZ S K", pathInCatalog="../../data/BOSS_DR10_kendrick_20150407/output/lowz_dr10_S_kendrick.txt", save=False)
#lowzSKendrick.plotHistograms()
#lowzSKendrick.plotFootprint()
#
#lowzNKendrick = Catalog(u, massConversion, name="lowz_n_kendrick", nameLong="LOWZ N K", pathInCatalog="../../data/BOSS_DR10_kendrick_20150407/output/lowz_dr10_N_kendrick.txt", save=False)
#lowzNKendrick.plotHistograms()
#lowzNKendrick.plotFootprint()
#
# combined catalog
lowzKendrick = lowzSKendrick.copy(name="lowz_kendrick", nameLong="LOWZ K")
#lowzKendrick.addCatalog(lowzNKendrick, save=False)
#lowzKendrick.plotHistograms()
#lowzKendrick.plotFootprint()

# BOSS = CMASS + LOWZ
bossKendrick = cmassSKendrick.copy(name="boss_kendrick", nameLong="BOSS K")
#bossKendrick.addCatalog(cmassNKendrick, save=False)
bossKendrick.addCatalog(lowzSKendrick, save=False)
#bossKendrick.addCatalog(lowzNKendrick, save=False)
#bossKendrick.plotHistograms()
#bossKendrick.plotFootprint()



###################################################################################
###################################################################################
# Read CMB maps

# CMB map name
cmbName = "tilecpactcmbkszd56"

# Planck + ACT
pathMap = "/global/cscratch1/sd/msyriac/data/depot/tilec/v1.0.0_rc_20190919/map_v1.0.0_rc_joint_deep56/" + "tilec_single_tile_deep56_cmb_map_v1.0.0_rc_joint.fits"

pathIn = "./output/cmb_map/tilec_pact_cmbksz_d56/"
pathHit = pathIn + "mask_foot_car.fits"
pathMask = pathIn + "mask_foot_planck_ps_car.fits"
pathPower = pathIn + "power_T_masked.txt"

tStart = time()
print "- Read CMB map, mask and hit count"
pactMap = enmap.read_map(pathMap)   # keep only temperature
pactMask = enmap.read_map(pathMask)
pactHit = enmap.read_map(pathHit)

tStop = time()
print "took", tStop-tStart, "sec"

# measured power spectrum
#data = np.genfromtxt(pathPower)  # l, Cl, sCl
#data = np.nan_to_num(data)
#fCl = interp1d(data[:,0], data[:,1], kind='linear', bounds_error=False, fill_value=0.)

# theory power spectrum
cmb1_6 = StageIVCMB(beam=1.6, noise=30., lMin=1., lMaxT=1.e5, lMaxP=1.e5, atm=False)


###################################################################################
###################################################################################
# Stacking


import thumbstack
reload(thumbstack)
from thumbstack import *


name = cmassMariana.name + "_" + cmbName 
tsCmassM = ThumbStack(u, cmassMariana, pactMap, pactMask, pactHit, name=name, nameLong=None, save=True, nProc=nProc)


###################################################################################

#name = cmassSMariana.name + "_" + cmbName 
#tsCmassSM = ThumbStack(u, cmassSMariana, pactMap, pactMask, pactHit, name=name, nameLong=None, save=True, nProc=nProc)

#name = cmassNMariana.name + "_" + cmbName 
#tsCmassNM = ThumbStack(u, cmassNMariana, pactMap, pactMask, pactHit, name=name, nameLong=None, save=True, nProc=nProc)

#name = cmassSKendrick.name + "_" + cmbName
#tsCmassSK = ThumbStack(u, cmassSKendrick, pactMap, pactMask, pactHit, name=name, nameLong=None, save=True, nProc=nProc)

#name = cmassNKendrick.name + "_" + cmbName
#tsCmassNK = ThumbStack(u, cmassNKendrick, pactMap, pactMask, pactHit, name=name, nameLong=None, save=True, nProc=nProc)

name = cmassKendrick.name + "_" + cmbName
tsCmassK = ThumbStack(u, cmassKendrick, pactMap, pactMask, pactHit, name=name, nameLong=None, save=True, nProc=nProc)

#name = lowzSKendrick.name + "_" + cmbName
#tsLowzSK = ThumbStack(u, lowzSKendrick, pactMap, pactMask, pactHit, name=name, nameLong=None, save=True, nProc=nProc)

#name = lowzNKendrick.name + "_" + cmbName
#tsLowzNK = ThumbStack(u, lowzNKendrick, pactMap, pactMask, pactHit, name=name, nameLong=None, save=True, nProc=nProc)

name = lowzKendrick.name + "_" + cmbName
tsLowzK = ThumbStack(u, lowzKendrick, pactMap, pactMask, pactHit, name=name, nameLong=None, save=True, nProc=nProc)

name = bossKendrick.name + "_" + cmbName
tsBossK = ThumbStack(u, bossKendrick, pactMap, pactMask, pactHit, name=name, nameLong=None, save=True, nProc=nProc)


###################################################################################
# Plot kSZ for the various samples


# plot CMASS Mariana
fig=plt.figure(0)
ax=fig.add_subplot(111)
#
# convert from sr to arcmin^2
factor = (180.*60./np.pi)**2
#
# CMASS M
ax.errorbar(tsCmassM.RApArcmin+0.02, factor * tsCmassM.kSZ, factor * np.sqrt(np.diag(tsCmassM.covKsz)), c='r', label=r'CMASS M')
ax.errorbar(tsCmassNM.RApArcmin, factor * tsCmassNM.kSZ, factor * np.sqrt(np.diag(tsCmassNM.covKsz)), fmt='--', c='r', alpha=0.2, label=r'CMASS N M')
ax.errorbar(tsCmassSM.RApArcmin+0.01, factor * tsCmassSM.kSZ, factor * np.sqrt(np.diag(tsCmassSM.covKsz)), fmt='-.', c='r', alpha=0.2, label=r'CMASS S M')
#
ax.legend(loc=2, fontsize='x-small', labelspacing=0.1)
ax.set_xlabel(r'$R$ [arcmin]')
ax.set_ylabel(r'$T_\text{kSZ}$ [$\mu K\cdot\text{arcmin}^2$]')
#ax.set_ylim((0., 2.))
#
path = tsCmassM.pathFig+"/ksz_cmass_mariana.pdf"
fig.savefig(path, bbox_inches='tight')
fig.clf()


# plot CMASS Kendrick
fig=plt.figure(0)
ax=fig.add_subplot(111)
#
# CMASS K
ax.errorbar(tsCmassK.RApArcmin+0.02, factor * tsCmassK.kSZ, factor * np.sqrt(np.diag(tsCmassK.covKsz)), c='r', label=r'CMASS K')
ax.errorbar(tsCmassNK.RApArcmin, factor * tsCmassNK.kSZ, factor * np.sqrt(np.diag(tsCmassNK.covKsz)), fmt='--', c='r', alpha=0.2, label=r'CMASS N K')
ax.errorbar(tsCmassSK.RApArcmin+0.01, factor * tsCmassSK.kSZ, factor * np.sqrt(np.diag(tsCmassSK.covKsz)), fmt='-.', c='r', alpha=0.2, label=r'CMASS S K')
#
ax.legend(loc=2, fontsize='x-small', labelspacing=0.1)
ax.set_xlabel(r'$R$ [arcmin]')
ax.set_ylabel(r'$T_\text{kSZ}$ [$\mu K\cdot\text{arcmin}^2$]')
ax.set_ylim((0., 10.))
#
path = tsCmassK.pathFig+"/ksz_cmass_kendrick.pdf"
fig.savefig(path, bbox_inches='tight')
fig.clf()


# plot LOWZ Kendrick
fig=plt.figure(0)
ax=fig.add_subplot(111)
#
ax.errorbar(tsLowzK.RApArcmin+0.02, factor * tsLowzK.kSZ, factor * np.sqrt(np.diag(tsLowzK.covKsz)), c='r', label=r'LOWZ K')
ax.errorbar(tsLowzNK.RApArcmin, factor * tsLowzNK.kSZ, factor * np.sqrt(np.diag(tsLowzNK.covKsz)), fmt='--', c='r', alpha=0.2, label=r'LOWZ N K')
ax.errorbar(tsLowzSK.RApArcmin+0.01, factor * tsLowzSK.kSZ, factor * np.sqrt(np.diag(tsLowzSK.covKsz)), fmt='-.', c='r', alpha=0.2, label=r'LOWZ S K')
#
ax.legend(loc=2, fontsize='x-small', labelspacing=0.1)
ax.set_xlabel(r'$R$ [arcmin]')
ax.set_ylabel(r'$T_\text{kSZ}$ [$\mu K\cdot\text{arcmin}^2$]')
#ax.set_ylim((0., 2.))
#
path = tsLowzK.pathFig+"/ksz_lowz_kendrick.pdf"
fig.savefig(path, bbox_inches='tight')
fig.clf()



# plot BOSS Kendrick
fig=plt.figure(0)
ax=fig.add_subplot(111)
#
# CMASS K
ax.errorbar(tsBossK.RApArcmin, factor * tsBossK.kSZ, factor * np.sqrt(np.diag(tsBossK.covKsz)), fmt='--', c='r', label=r'BOSS K')
#
ax.legend(loc=2, fontsize='x-small', labelspacing=0.1)
ax.set_xlabel(r'$R$ [arcmin]')
ax.set_ylabel(r'$T_\text{kSZ}$ [$\mu K\cdot\text{arcmin}^2$]')
#ax.set_xlim((0., 2.))
#
path = tsBossK.pathFig+"/ksz_kendrick.pdf"
fig.savefig(path, bbox_inches='tight')
fig.clf()



###################################################################################
# Plot tSZ for the various samples


# plot CMASS Mariana
fig=plt.figure(0)
ax=fig.add_subplot(111)
#
# convert from sr to arcmin^2
factor = (180.*60./np.pi)**2
#
# CMASS M
ax.errorbar(tsCmassM.RApArcmin+0.02, factor * tsCmassM.tSZ, factor * np.sqrt(np.diag(tsCmassM.covTsz)), c='r', label=r'CMASS M')
ax.errorbar(tsCmassNM.RApArcmin, factor * tsCmassNM.tSZ, factor * np.sqrt(np.diag(tsCmassNM.covTsz)), fmt='--', c='r', alpha=0.2, label=r'CMASS N M')
ax.errorbar(tsCmassSM.RApArcmin+0.01, factor * tsCmassSM.tSZ, factor * np.sqrt(np.diag(tsCmassSM.covTsz)), fmt='-.', c='r', alpha=0.2, label=r'CMASS S M')
#
ax.legend(loc=1, fontsize='x-small', labelspacing=0.1)
ax.set_xlabel(r'$R$ [arcmin]')
ax.set_ylabel(r'$T_\text{tSZ}$ [$\mu K\cdot\text{arcmin}^2$]')
#ax.set_ylim((0., 2.))
#
path = tsCmassM.pathFig+"/tsz_cmass_mariana.pdf"
fig.savefig(path, bbox_inches='tight')
fig.clf()


# plot CMASS Kendrick
fig=plt.figure(0)
ax=fig.add_subplot(111)
#
# CMASS K
ax.errorbar(tsCmassK.RApArcmin+0.02, factor * tsCmassK.tSZ, factor * np.sqrt(np.diag(tsCmassK.covTsz)), c='r', label=r'CMASS K')
ax.errorbar(tsCmassNK.RApArcmin, factor * tsCmassNK.tSZ, factor * np.sqrt(np.diag(tsCmassNK.covTsz)), fmt='--', c='r', alpha=0.2, label=r'CMASS N K')
ax.errorbar(tsCmassSK.RApArcmin+0.01, factor * tsCmassSK.tSZ, factor * np.sqrt(np.diag(tsCmassSK.covTsz)), fmt='-.', c='r', alpha=0.2, label=r'CMASS S K')
#
ax.legend(loc=1, fontsize='x-small', labelspacing=0.1)
ax.set_xlabel(r'$R$ [arcmin]')
ax.set_ylabel(r'$T_\text{tSZ}$ [$\mu K\cdot\text{arcmin}^2$]')
#ax.set_ylim((0., 10.))
#
path = tsCmassK.pathFig+"/tsz_cmass_kendrick.pdf"
fig.savefig(path, bbox_inches='tight')
fig.clf()


# plot LOWZ Kendrick
fig=plt.figure(0)
ax=fig.add_subplot(111)
#
# CMASS K
ax.errorbar(tsLowzK.RApArcmin+0.02, factor * tsLowzK.tSZ, factor * np.sqrt(np.diag(tsLowzK.covTsz)), c='r', label=r'LOWZ K')
ax.errorbar(tsLowzNK.RApArcmin, factor * tsLowzNK.tSZ, factor * np.sqrt(np.diag(tsLowzNK.covTsz)), fmt='--', c='r', alpha=0.2, label=r'LOWZ N K')
ax.errorbar(tsLowzSK.RApArcmin+0.01, factor * tsLowzSK.tSZ, factor * np.sqrt(np.diag(tsLowzSK.covTsz)), fmt='-.', c='r', alpha=0.2, label=r'LOWZ S K')
#
ax.legend(loc=1, fontsize='x-small', labelspacing=0.1)
ax.set_xlabel(r'$R$ [arcmin]')
ax.set_ylabel(r'$T_\text{tSZ}$ [$\mu K\cdot\text{arcmin}^2$]')
#ax.set_ylim((0., 2.))
#
path = tsLowzK.pathFig+"/tsz_lowz_kendrick.pdf"
fig.savefig(path, bbox_inches='tight')
fig.clf()


# plot BOSS Kendrick
fig=plt.figure(0)
ax=fig.add_subplot(111)
#
# CMASS K
ax.errorbar(tsBossK.RApArcmin, factor * tsBossK.tSZ, factor * np.sqrt(np.diag(tsBossK.covTsz)), fmt='--', c='r', label=r'BOSS K')
#
ax.legend(loc=1, fontsize='x-small', labelspacing=0.1)
ax.set_xlabel(r'$R$ [arcmin]')
ax.set_ylabel(r'$T_\text{tSZ}$ [$\mu K\cdot\text{arcmin}^2$]')
#ax.set_xlim((0., 2.))
#
path = tsBossK.pathFig+"/tsz_kendrick.pdf"
fig.savefig(path, bbox_inches='tight')
fig.clf()
