python ~/working/prog_scripts/realslice_reducer.py chi_extrapolated.dat
 python ~/working/prog_scripts/ME_prep_james_lessfast.py $1 chi_slices.dat
 python ~/working/prog_scripts/peakfinder_slice.py realfreq.dat
python ~/working/prog_scripts/peakslice_plots.py peaks_slice.dat
python ~/working/prog_scripts/lambdaslice_plots.py lambda_slice.dat
sh ~/working/prog_scripts/slice_combine.sh
