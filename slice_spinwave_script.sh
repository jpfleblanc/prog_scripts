python ~/working_2017/prog_scripts/extract_DF.py
python ~/working_2017/prog_scripts/extract_DF_chi.py
python ~/working_2017/prog_scripts/dmft_GG_correction_correct_chi.py ../../G_omegareal_18 ../../G_omega_18 64 1024 32 20 chi_file.dat
python ~/working_2017/prog_scripts/realslice_reducer.py chi_corrected.dat #chi_file.dat
 python ~/working_2017/prog_scripts//ME_prep_james_lessfast.py 5.0 chi_slices.dat
 python ~/working_2017/prog_scripts/peakfinder_slice.py realfreq.dat
python ~/working_2017/prog_scripts/peakslice_plots.py peaks_slice.dat

