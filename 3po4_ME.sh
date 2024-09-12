awk '$1==2.356194490192344837e+00 && $2==0 {print}' chi_extrapolated.dat > chi_3po4.dat
timeout 35 python ~/working/prog_scripts/ME_prep_james_lessfast.py $1 chi_3po4.dat
 python ~/working/prog_scripts/peakfinder_slice.py realfreq.dat
#python ~/working/prog_scripts/peakslice_plots.py peaks_slice.dat
#python ~/working/prog_scripts/lambdaslice_plots.py lambda_slice.dat
#sh ~/working/prog_scripts/slice_combine.sh
