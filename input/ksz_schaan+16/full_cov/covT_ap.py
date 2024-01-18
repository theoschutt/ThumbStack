import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad


# theta0 in arcmin
theta0Arcmin = np.array([ 0.52789248,  1.05578496,  1.58367744,  2.11156992,  2.6394624 ,
                         3.16735489,  3.69524737,  4.22313985])


# detector sensitivity in muK*rad. (13 muK.arcmin from a non-reliable source)
#sensitivity = 13.*(np.pi/180.)/60.
sensitivity = 12.7*(np.pi/180.)/60.

# theta, theta0 in rad
def W(theta, theta0):
   result = (theta>0.)*(theta<theta0) / (np.pi*theta0**2)
   result -= (theta>theta0)*(theta<np.sqrt(2.)*theta0) / (np.pi*theta0**2)
   return result

def plotW(theta0=0.5):
   Theta = np.linspace(0., 1., 101)
   fW = lambda t: W(t, theta0)
   WW = map(fW, Theta)
   
   plt.figure(0)
   #
   plt.plot(Theta, WW)

   plt.show()


def computeCov(i,j):
   theta1 = theta0Arcmin[i] * np.pi/(180.*60.)
   theta2 = theta0Arcmin[j] * np.pi/(180.*60.)

   f = lambda t: 2.*np.pi*t * W(t, theta1)*W(t, theta2)
   result = quad(f, 0., np.sqrt(2.)*max(theta1, theta2), epsabs=0., epsrel=1.e-3)[0]
   result *= sensitivity**2
   return result


def saveCov():
   N = len(theta0Arcmin)
   Cov = np.zeros((N, N))

   for i in range(N):
      for j in range(N):
         Cov[i,j] = computeCov(i,j)

   return Cov


def plotCov():
   Cov = saveCov()

   plt.imshow(Cov, interpolation='nearest')
   plt.colorbar()
   plt.show()


   plt.plot(theta0Arcmin, np.sqrt(np.diagonal(Cov)))
   plt.xlabel(r'$\theta_0$ [arcmin]')
   plt.ylabel(r'std. dev. of AP filter [$\mu$K]')
   plt.show()

   np.savetxt("covT_12.7muKarcmin.txt", Cov)



