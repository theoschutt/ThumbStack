#from pylab import *


import numpy as np
import matplotlib.pyplot as plt
import os
# to copy files
from shutil import copyfile
from scipy import special, optimize, integrate, stats
from scipy.interpolate import UnivariateSpline, RectBivariateSpline, interp1d, interp2d, BarycentricInterpolator
from time import time
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
from matplotlib.colors import LogNorm
import matplotlib.colors as mc
import colorsys
from timeit import timeit
from time import time
from copy import copy
import sys
from mpmath import polylog


# For CMB maps
#from enlib import enmap, utils, powspec
from pixell import enmap, utils, powspec, enplot, reproject #, pointsrcs
import healpy as hp
# copy rotfuncs.py somewhere on your python path,
# so you can import it
import rotfuncs





# parallelizing "map"
# version that works when the function is a class module
#from pathos.multiprocessing import ProcessingPool as Pool
#from multiprocess import Pool

# Yu Feng's version of multiprocessing, relying on forking rather than pickling
import sharedmem

#import vegas   # for Monte Carlo integration, for CMB lens reconstruction
#import gvar as gv
from astropy.io import fits   # for saving/reeading maps
import colormaps as cmaps  # for viridis and plasma colormaps

# to save wav files
from scipy.io import wavfile

# for faster FFT
#import pyfftw
import importlib
#pyfftw.interfaces.cache.enable() # so subsequent FFTs use the wisdom from the first one
## however, this wisdom is only kept for 0.1sec, or for x seconds if using:
##pyfftw.interfaces.cache.set_keepalive_time(x)


# neutrino masses: https://github.com/ThomasTram/iCLASS/blob/master/neutrinohierarchy.ipynb
# cosmo doc: https://lesgourg.github.io/class-tour/Narbonne.pdf
from classy import Class

# http://classylss.readthedocs.io/en/stable/index.html
import classylss
import classylss.binding as CLASS

import healpy as hp

##################################################################################
# for pretty plots

from matplotlib import rc
#rc('font',**{'size':'20','family':'sans-serif','sans-serif':['Computer Modern Sans serif']})
# rc('font',**{'size':'22','family':'serif','serif':['CMU serif']})
# rc('mathtext', **{'fontset':'cm'})
# rc('text', usetex=True)
# rc('text.latex', preamble="\\usepackage{amsmath}, \\usepackage{amssymb}")
#rc('font', size=20)
# rc('legend',**{'fontsize':'18'})

# fonty stuffs
#font.serif: CMU Serif
#font.family: serif
#mathtext.fontset: cm
#text.usetex: False
#text.latex.preamble: \usepackage{amsmath}

def darkerLighter(color, amount=0.):
   """
   Adapted from https://stackoverflow.com/questions/37765197/darken-or-lighten-a-color-in-matplotlib
   Input can be matplotlib color string, hex string, or RGB tuple.
   amount=0: color unchanged
   amount=-1: returns white
   amount=1: returns black

   Examples:
   >> lighten_color('g', 0.3)
   >> lighten_color('#F034A3', 0.6)
   >> lighten_color((.3,.55,.1), 0.5)
   """
   # force amount between 0. and 1.
   amount = min(amount, 1.)
   amount = max(amount, -1.)
   # read the color
   try:
      c = mc.cnames[color]
   except:
      c = color
   c = colorsys.rgb_to_hls(*mc.to_rgb(c))
   # my Lagrange interpolation polynomial
   newC1 = 0.5*amount*(amount-1.) - c[1]*(amount+1.)*(amount-1.)
   return colorsys.hls_to_rgb(c[0], newC1, c[2])


##################################################################################

import basic_functions
importlib.reload(basic_functions)
from basic_functions import *

import flat_map
importlib.reload(flat_map)
from flat_map import *

