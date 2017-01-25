python ~/working_2017/prog_scripts/realslice_reducer.py chi_extrapolated.dat
 python ~/working_2017/prog_scripts/ME_prep_james_lessfast.py 5.0 chi_slices.dat
 python ~/working_2017/prog_scripts/peakfinder_slice.py realfreq.dat
python ~/working_2017/prog_scripts/peakslice_plots.py peaks_slice.dat
python ~/working_2017/prog_scripts/lambdaslice_plots.py lambda_slice.dat
sh ~/working_2017/prog_scripts/slice_combine.sh
