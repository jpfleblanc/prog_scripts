import math,zlib,numpy,sys
chi=sys.argv[2]
f1 = open(chi+'_fitting_real_sumQ.dat','w')
f2 = open(chi+'_fitting_imag_sumQ.dat','w')
w_start=27
w_end=32
w_num=w_end-w_start+1
v_num=21
beta=float(sys.argv[1])
print beta
x=[0]*w_num #x stores omega^-1
y1=[[0 for i in range(w_num)] for i in range(v_num)] #y1 stores chi_real
y2=[[0 for i in range(w_num)] for i in range(v_num)] #y2 stores chi_imag
for omegac in range(w_start,w_end+1):
  x[omegac-w_start]=beta/(2.0*omegac+1)/3.1415926
  with open(chi+'_m_'+str(omegac)) as file:
    array2d = [[float(digit) for digit in line.split()] for line in file]
  for nu in range(v_num):
    for site in range(8):
      y1[nu][omegac-w_start]+=array2d[nu][2*site]
      y2[nu][omegac-w_start]+=array2d[nu][2*site+1]

for nu in range(v_num):
  coefficient = numpy.polyfit(x,y1[nu],1)
  poly = numpy.poly1d(coefficient)
  extrapo_chi = poly(0) 
  print nu,extrapo_chi
  f1.write(str(2*(nu-10)*3.1415926/beta)+" "+str(extrapo_chi)+"\n")
f1.close()

for nu in range(v_num):
  coefficient = numpy.polyfit(x,y2[nu],1)
  poly = numpy.poly1d(coefficient)
  extrapo_chi = poly(0) 
  print nu,extrapo_chi
  f2.write(str(2*(nu-10)*3.1415926/beta)+" "+str(extrapo_chi)+"\n")
f2.close()

f = open(chi+'_diff_cut_omega_sum_sumQ.dat','w')
for omegac in range(w_start,w_end+1):
  f.write(str(x[omegac-w_start])+" ")
  for nu in range(v_num):
    f.write(str(y1[nu][omegac-w_start])+" ")
    f.write(str(y2[nu][omegac-w_start])+" ")
  f.write("\n")
f.close()
