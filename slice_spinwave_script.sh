python ~/working_2016/nikolay_requests/prog_scripts/extract_DF.py
python ~/working_2016/nikolay_requests/prog_scripts/extract_DF_chi.py
python ~/working_2016/nikolay_requests/prog_scripts/realslice_reducer.py chi_file.dat
 python ~/working_2016/nikolay_requests/prog_scripts/ME_prep_james_lessfast.py 5.0 chi_slices.dat
 python ~/working_2016/nikolay_requests/prog_scripts/peakfinder_slice.py realfreq.dat
python ~/working_2016/nikolay_requests/prog_scripts/peakslice_plots.py peaks_slice.dat