import numpy as np
import matplotlib.pyplot as plt

# We use an aperture photometry filter, with radius theta0
# and a ring with radius sqrt(2)*theta0.
# theta0 is given below, in arcmin and in Mpc/h at z=0.57 (you can check)
# The covariance matrix for these theta0 is given below too.

# theta0 in arcmin
theta0Arcmin = np.array([ 0.52789248,  1.05578496,  1.58367744,  2.11156992,  2.6394624 ,
        3.16735489,  3.69524737,  4.22313985])


# theta0 in Mpc/h, at z=0.57
theta0Mpch = np.array([ 0.22817499,  0.45634998,  0.68452496,  0.91269995,  1.14087494,
        1.36904993,  1.59722492,  1.8253999 ])

# cov matrix for Mariana's velocities,
# with 25,537 objects (CMASS galaxies)
cov = np.genfromtxt("cov_mariana_25537.txt")

# plot the covariance matrix
plt.figure(0)
plt.imshow(cov, interpolation='nearest')


# just to check, to recover the plot in our paper,
# compute the correlation coefficient.
# The plot in the paper is missing the smallest aperture size (because we found no signal there, so we didn't include it).
n = len(cov[:,0])
cor = np.zeros_like(cov)
for i in range(n):
    for j in range(n):
        cor[i,j] = cov[i,j] / np.sqrt(cov[i,i]*cov[j,j])


# plot the correlation coefficients (as in the paper)
plt.figure(1)
plt.imshow(cor, interpolation='nearest')

plt.show()
