










import sys

import sys, getopt;
import os, os.path, shutil, distutils.dir_util,numpy,h5py
from numpy import array,average
import re
import math
import resource


def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)


def main(argv):


	nfermi=str(sys.argv[1])

	os.system("python ~/working/prog_scripts/extract_DF_chi.py")
	os.system("~/working/prog_scripts/bubble_code/bubble --input_dmft_file ../../Greens_17.h5 --input_df_file output.h5 --kpts 16 --nfermi "+nfermi+" --nbose 33 --beta 5 --output_file bubble.h5")
	os.system("python ~/working/prog_scripts/extract_bubble_chi.py")


	

if __name__ == "__main__":
    main(sys.argv[1:])



