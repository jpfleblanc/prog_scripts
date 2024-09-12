import math,zlib,numpy,sys
beta = float(sys.argv[1])
chi = sys.argv[2]
parm_file=open("maxent_"+chi+".parm",'w')
dat_file=open("dat_in",'w')
with open(chi+'_real_QPIPI.dat') as file:
  real_array = [[float(digit) for digit in line.split()] for line in file]
with open(chi+'_imag_QPIPI.dat') as file:
  imag_array = [[float(digit) for digit in line.split()] for line in file]

real = real_array
imag = imag_array
norm = real_array[10][1]

parm_file.write("N_ALPHA = 40\nALPHA_MIN = 0.05\nALPHA_MAX = 5\n")
parm_file.write("NORM = "+str(norm)+"\n")
parm_file.write("OMEGA_MAX = 40\n")
parm_file.write("KERNEL = bosonic\n")
parm_file.write("BETA = "+str(beta)+"\n")
parm_file.write("NFREQ = 1000\n")
parm_file.write("NDAT = 22\n")
parm_file.write("FREQUENCY_GRID = Lorentzian\n")
parm_file.write("DATASPACE =frequency\n")
parm_file.write("MAX_IT = 2000\n")
parm_file.write("DEFAULT_MODEL =\"gaussian\"\n")
parm_file.write("TEXT_OUTPUT = 1\n")
parm_file.write("SELF = 0\n")
parm_file.write("SIGMA = 3\n")
parm_file.write("PARTICLE_HOLE_SYMMETRY = 0\n")
parm_file.write("DATA = dat_in0\n")

for n in range(11):
  parm_file.write(str(real[n+10][0])+" "+str(real[n+10][1])+" "+str(real[n+10][2])+" "+str(imag[n+10][1])+" "+str(imag[n+10][2])+"\n")

parm_file.close()

