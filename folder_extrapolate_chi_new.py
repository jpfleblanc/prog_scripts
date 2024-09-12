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
	temp_mu_folders_filtered=[]
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
	rerun_inverter=False
	run_anyways=False

	max_number=1000
	current_number=0

# ---------------- Now move into Betts directories


	for item in site_folderlist:
		os.chdir(start_directory + "/"+ item)
		print("cd " + start_directory + "/"+ item)
		print("I am in " + os.getcwd())
		temp_mu_folders=filter(os.path.isdir, os.listdir('.'))
		for temp_item in temp_mu_folders:
			if "-ref" not in dir_items and "backup" not in temp_item:
				temp_mu_folders_filtered.append(temp_item)

		print temp_mu_folders_filtered
# --------- check for sim.h5 files
		for folder_item in temp_mu_folders_filtered:
			print os.getcwd()
			print start_directory + "/"+ item+"/"+folder_item+"/sim.h5"

			if os.path.exists(start_directory + "/"+ item+"/"+folder_item+"/sim.h5"):
				f = h5py.File(start_directory + "/"+ item+"/"+folder_item+"/sim.h5", 'r')
				mu=f["/parameters/dictionary/MU"].value
				site=f["/parameters/dictionary/dca.SITES"].value
				beta=f["/parameters/dictionary/BETA"].value
				T=1.0/float(beta)
				nfreq=f["/parameters/dictionary/NMATSUBARA"].value	
				Uvalue=f["/parameters/dictionary/U"].value	
				tprime=f["/parameters/dictionary/tprime"].value
				tdprime=f["/parameters/dictionary/tdprime"].value

			
			print "folder item is "+ folder_item
			os.chdir(start_directory + "/"+ item+"/"+folder_item+"/vertex_run")
			print start_directory + "/"+ item+"/"+folder_item+"/vertex_run"

			big_f=64
			inputdir_big = os.getcwd()+"/run_DF_nogg"
			small_f=48
			inputdir_small = os.getcwd()+"/run_DF_nogg-nfsmall"
			print inputdir_big+"/output.h5", os.path.exists(inputdir_big+"/output.h5"),inputdir_small+"/output.h5", os.path.exists(inputdir_small+"/output.h5")
			
			if os.path.exists(os.getcwd()+"/chi_extrapolated.dat")==False:
				if os.path.exists(inputdir_big+"/output.h5") and os.path.exists(inputdir_small+"/output.h5"):
<<<<<<< HEAD
					os.system("python ~/working/prog_scripts/extrapolate_chi_new.py "+str(big_f)+ " "+ inputdir_big + " "+ str(small_f)+ " " +inputdir_small+" " +str(beta))    
	
=======
					f2 = h5py.File(inputdir_big+"/output.h5", 'r')
					kpts=f2["/df/parameters/kpts"].value
					os.system("python ~/working/prog_scripts/extrapolate_chi.py "+str(big_f)+ " "+ inputdir_big + " "+ str(small_f)+ " " +inputdir_small+" " +str(beta)+" " +str(kpts))   
>>>>>>> c6cd297a502ed28fc881b6211d81c7a64c57b32e
			




	

if __name__ == "__main__":
    main(sys.argv[1:])






