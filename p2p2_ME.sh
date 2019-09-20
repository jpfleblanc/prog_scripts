awk '$1==1.570796326794896558e+00 && $2==$1 {print}' chi_extrapolated.dat > chi_pipi.dat
timeout 180 python ~/working/prog_scripts/ME_prep_james_lessfast.py $1 chi_pipi.dat
python ~/working/prog_scripts/peakfinder_slice.py realfreq.dat
#python ~/working/prog_scripts/peakslice_plots.py peaks_slice.dat
#python ~/working/prog_scripts/lambdaslice_plots.py lambda_slice.dat
#sh ~/working/prog_scripts/slice_combine.sh
