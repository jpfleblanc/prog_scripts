awk '$1==3.141592653589793116e+00 && $2==$1 {print}' chi_extrapolated.dat > chi_pipi.dat
<<<<<<< HEAD
timeout 35 python ~/working_2017/prog_scripts/ME_prep_james_lessfast.py $1 chi_pipi.dat
 python ~/working_2017/prog_scripts/peakfinder_slice.py realfreq.dat
=======
timeout 180 python ~/working/prog_scripts/ME_prep_james_lessfast.py $1 chi_pipi.dat
python ~/working/prog_scripts/peakfinder_slice.py realfreq.dat
>>>>>>> c6cd297a502ed28fc881b6211d81c7a64c57b32e
#python ~/working/prog_scripts/peakslice_plots.py peaks_slice.dat
#python ~/working/prog_scripts/lambdaslice_plots.py lambda_slice.dat
#sh ~/working/prog_scripts/slice_combine.sh
