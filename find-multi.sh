find . -name 'ctaux.param' -print0 -exec echo {} \; -exec grep 'MU =' {} \; > muvals.dat
