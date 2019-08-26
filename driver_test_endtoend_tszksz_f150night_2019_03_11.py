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
#plt.switch_backend('Agg')

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
cmassNMariana = Catalog(u, massConversion, name="cmass_n_mariana", nameLong="CMASS N M", pathInCatalog="../../data/CMASS_DR12_mariana_20160200/output/cmass_dr12_N_mariana.txt", save=False)
#cmassNMariana.plotHistograms()
#cmassNMariana.plotFootprint()
#cmassMariana.printProperties()
#
# combined catalog
cmassMariana = cmassSMariana.copy(name="cmass_mariana", nameLong="CMASS M")
cmassMariana.addCatalog(cmassNMariana, save=False)
#cmassMariana.plotHistograms()
#cmassMariana.plotFootprint()
#cmassMariana.printProperties()



###################################################################################
###################################################################################
# Read CMB maps: map, mask, hit count map

# directory of mocks
pathMock = "/global/cscratch1/sd/eschaan/project_ksz_act_planck/data/mock_maps_CMASS_DR12_mariana/"
pathMap = pathMock + "CMASS_COUNTS_SMOOTH1.5_8192_car.fits"
#pathMap = pathMock + "CMASS_VEL_SMOOTH1.5_8192.fits"

# path to true hit count map and mask: Planck + ACT 150GHz day and night
pathIn = "/global/cscratch1/sd/eschaan/project_ksz_act_planck/data/planck_act_coadd_2019_03_11/"
pathHit = pathIn + "act_planck_f150_prelim_div_mono.fits"
pathMask = pathIn + "f150_mask_foot_planck_ps_car.fits"
pathPower = pathIn + "f150_power_T_masked.txt"

# read maps in common for all mocks
pact150Mask = enmap.read_map(pathMask)
pact150Hit = enmap.read_map(pathHit)
pact150Map = enmap.read_map(pathMap)[0]   # keep only temperature

# theory power spectrum
cmb1_4 = StageIVCMB(beam=1.4, noise=30., lMin=1., lMaxT=1.e5, lMaxP=1.e5, atm=False)


###################################################################################


import thumbstack
reload(thumbstack)
from thumbstack import *

# Stacking
name = cmassMariana.name + "_pactf150night20190311_test_endtoend_counts"
tsCmassM = ThumbStack(u, cmassMariana, pact150Map, pact150Mask, pact150Hit, name=name, nameLong=None, save=True, nProc=nProc)


#tsCmassM.analyzeObject(0, test=True)
tsCmassM.examineCmbMaps()


tsCmassM.plotTszKsz()
tsCmassM.compareKszEstimators()
tsCmassM.computeSnrTsz()
tsCmassM.computeSnrKsz()
tsCmassM.kszNullTests()
tsCmassM.plotCovTszKsz()



###################################################################################
