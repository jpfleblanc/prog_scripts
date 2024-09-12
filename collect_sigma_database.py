import sys
#uncomment to run on garching
#sys.path.append('/u/jleblanc/software/h5py-2.0.1/base/usr/local/lib64/python2.6/site-packages')
import sys, getopt;
import os, os.path, shutil, distutils.dir_util,numpy,h5py
from numpy import array,average
import re
import math
import resource

#from evalnnsisj import *

#from linreg import linreg

#from collections import namedtuple

#simStructure = namedtuple("simStructure", "density mu sites")

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)


def main(argv):
#  U="8"
#  LATTICE="Betts2D-1A"
#  SITES=1
#  try:                                
#    opts, args = getopt.getopt(argv, "hULs", ["help", "U=", "lattice=","sites="])
#  except getopt.GetoptError:          
#    usage()                         
#    sys.exit(2)                     
#  for opt, arg in opts:
#    if opt in ("-h", "--help"):
#      usage()                     
#      sys.exit()                  
#    elif opt in("-L","--lattice"):
#      LATTICE = arg                 
#    elif opt in ("-U", "--U"):
#      U = arg 
#    elif opt in ("-s", "--sites"):
#      SITES =arg 
  resource.setrlimit(resource.RLIMIT_NOFILE, (4096, 4096))
  eval()

def usage():
  print("call program with -U for U, --sites= for # sites, --lattice= for lattice")

def eval():
 
	sitelist=[]
	site_folderlist=[]

	fileslist=[]

	temp_mu_folders=[]
	fig1b=[]

	start_directory=os.getcwd()
	print("Starting in "+start_directory)
	
	files = filter(os.path.isfile, os.listdir('.')) 
	dirs = filter(os.path.isdir, os.listdir('.'))  

	print("Files are " +str(files))
	print("Directories are " +str(dirs))

	for dir_items in dirs:
		print("Directories are "+ dir_items)
		
	for dir_items in dirs:
		if "Betts2D" in dir_items:
			print("Betts folders are " + dir_items)
			if "-ref" not in dir_items and "backup" not in dir_items:
				site_folderlist.append(dir_items)
			sitenum=dir_items[8:-1].strip()			
			sitelist.append(sitenum)	
  	print sitelist	
	sitelist=natural_sort(sitelist)
	site_folderlist=natural_sort(site_folderlist)
	print("Available site folders are ")
	print site_folderlist

	rerun_DF=False

	database=[]

# ---------------- Now move into Betts directories


	for item in site_folderlist:
		os.chdir(start_directory + "/"+ item)
		print("cd " + start_directory + "/"+ item)
		print("I am in " + os.getcwd())
		temp_mu_folders=filter(os.path.isdir, os.listdir('.'))
		

# --------- check for sim.h5 files
		for folder_item in temp_mu_folders:

			if os.path.exists(start_directory + "/"+ item+"/"+folder_item+"/vertex_run"):
				os.chdir(start_directory + "/"+ item+"/"+folder_item+"/vertex_run")
				print("I am in " + os.getcwd())
				if os.path.exists(os.getcwd()+"/sim.h5"):
					#print("sim.h5 exists in folder"+os.getcwd()+"/"+folder_item+"/sim.h5")
				
				
	#--------- read in relevant data from sim.h5
					f = h5py.File(os.getcwd()+"/sim.h5", 'r')
					mu=float(f["/parameters/dictionary/MU"].value)
					beta=f["/parameters/dictionary/BETA"].value
					T=1.0/float(beta)
					Uvalue=float(f["/parameters/dictionary/U"].value	)

				if os.path.exists(os.getcwd()+"/run_DF_nogg"):
					os.chdir(os.getcwd()+"/run_DF_nogg")
					os.system("python ~/working/prog_scripts/extract_DF.py")
					if os.path.exists(os.getcwd()+"/sigma_output_nodal.dat"):
						w, sigma_node = numpy.loadtxt("sigma_output_nodal.dat", usecols=(0,4), unpack=True)
						w, sigma_antinode = numpy.loadtxt("sigma_output_antinodal.dat", usecols=(0,4), unpack=True)
	
						database.append((Uvalue, T, mu, sigma_node[0], sigma_node[1], sigma_antinode[0], sigma_antinode[1]))




	os.chdir(start_directory)
	numpy.savetxt("sigma_database.dat",database)


	
			




	

if __name__ == "__main__":
    main(sys.argv[1:])






