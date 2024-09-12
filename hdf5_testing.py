import sys, getopt;
import os, os.path, shutil, distutils.dir_util,numpy,h5py


f = h5py.File(os.getcwd()+"/sim.h5", 'r')

results=[]

mu=f["/parameters/dictionary/MU"].value
site=f["/parameters//dictionary/dca.SITES"].value
beta=f["/parameters//dictionary/BETA"].value

sz=f["/simulation/results/Sz/mean/value"][0]

results.append((mu,site,beta,sz))

print results

numpy.savetxt("collected.dat",results)


