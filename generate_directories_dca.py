#this script generates the file names
from os import system

import sys
#uncomment to run on garching
#sys.path.append('/u/jleblanc/software/h5py-2.0.1/base/usr/local/lib64/python2.6/site-packages')
import sys, getopt
import os, os.path, shutil, distutils.dir_util,numpy,h5py
from numpy import array,average
import re
import math


def main(argv):


  eval()

def eval():


  database_filename=sys.argv[1]

  newdata=[]


  read_file=open(database_filename, 'r')
  U_val, T_val, mu_val, etotal_val,site_val, D_val, D_err_val, density_val, density_err_val, sign_val , ekin_err_val, epot_err_val, tprime_val= numpy.loadtxt(read_file,  usecols= (0, 1,2,3,4,5,6, 11, 12, 17, 8, 10, 18 ) ,unpack=True)
  read_file.close()

  print density_val

	#print a[14][0]
	#print len(a[0])

  for x in range(0, len(U_val)-1):
    newdata.append((U_val[x], T_val[x], mu_val[x], etotal_val[x],site_val[x],D_val[x], D_err_val[x], density_val[x]*sign_val[x], density_err_val[x]*sign_val[x], sign_val[x], ekin_err_val[x], epot_err_val[x], tprime_val[x]))




  for t in ["1"]:
    for tprime in ["-0.2","0","0.2"]:
      ttprime="t"+t+"_tprime"+tprime
      print ttprime
      system("mkdir -p "+ttprime)
      for U in ["2","4","6","8","12"]:
        for n in ["1","0.875","0.8","0.6","0.3"]:
          for T in ["0","0.125","0.25","0.5"]:
            filename= "t"+t+"_tprime"+tprime+"_U"+U+"_n"+n+"_T"+T
          #  print filename
            system("mkdir -p "+ttprime+"/" +filename)
            pwd= ttprime+"/"+filename


            

            for item in newdata:
           #   print "Hello",  abs(float(tprime)-item[12]) < 0.001 , abs(float(U)-item[0]) < 0.001 , abs(float(n)-item[7])<0.001 , abs(float(T)-item[1]) < 0.001
              if abs(float(tprime)-item[12]) < 0.001 and abs(float(U)-item[0]) < 0.001 and abs(float(n)/2.0-item[7]) < 0.01 and abs(float(T)-item[1]) < 0.01:
                
                
		print "Found for"
		print tprime, U, n, T
# catch tprime issue at half filling
                if abs(item[7]-0.5)<0.001 and abs(item[12] - 0.0) < 0.001:
                  print t, tprime, U, n, T 
                  print "Writing to "+ pwd+"/E_DCA_size"+str(item[4])

# not 100% sure that this shouldn't be item[3]+2.0*item[2]*(0.5-item[7])  #-item[0]*(0.5-item[7])
                  energy_output= item[3]-2.0*item[2]*(0.5-item[7])-item[0]*(0.5-item[7])
                  os.system("echo "+ str(item[7]*2.0)  +" "+ str(item[8]*2.0)+" "+ str(energy_output) +" " +str( math.sqrt(item[10]*item[10] + item[11]*item[11]) ) +" > "+ pwd+"/E_DCA_size"+str(item[4]) )
                  #if math.isnan(item[6]) is False:
                  os.system("echo "+ str(item[7]*2.0)  +" "+ str(item[8]*2.0)+" "+ str(item[5]) +" " +str( item[6]) +" > "+ pwd+"/D_DCA_size"+str(item[4]) )




# not half filled
                if abs(item[7]-0.5)>0.001:
                  energy_output= item[3]-2.0*item[2]*(0.5-item[7])-item[0]*(0.5-item[7])
                  print t, tprime, U, n, T 
                  print "Writing to "+ pwd+"/E_DCA_size"+str(item[4])
                  os.system("echo "+ str(item[7]*2.0)  +" "+ str(item[8]*2.0)+" "+ str(energy_output) +" " +str( math.sqrt(item[10]*item[10] + item[11]*item[11]) ) +" > "+ pwd+"/E_DCA_size"+str(item[4]) )
                  print item[6]
                  #if math.isnan(item[6]*2) is False:
                  os.system("echo "+ str(item[7]*2.0)  +" "+ str(item[8]*2.0)+" "+ str(item[5]) +" " +str( item[6]) +" > "+ pwd+"/D_DCA_size"+str(item[4]) )

          



if __name__ == "__main__":
    main(sys.argv[1:])

          



