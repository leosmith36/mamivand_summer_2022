#!/bin/bash

OLDIFS=$IFS # save original IFS setting
IFS=','

## reading data from CSV file
while read -r a b c d; do
	m22+=("$a")
	m33+=("$b")
	m23+=("$c")
	k+=("$d")
done < input_data.csv
IFS=$OLDIFS # restore orig setting

cr=0.329
co=0.216
temp=873

## Define tol for finding min and max in the MOOSE input file
tol=0.001

## For loop for running all the jobs over super computer (R2 or Borah)

for i in {48..95} ##all rows ${#cr[*]} 
do
	## Make a directory for new job with its name
	mkdir run_m22_${m22[$i]}_m33_${m33[$i]}_m23_${m23[$i]}_k_${k[$i]}
	
	## Copy all the required files to new directory
	cp -R build include Makefile scripts test doc lib README.md db2-opt LICENSE run_tests src ./run_m22_${m22[$i]}_m33_${m33[$i]}_m23_${m23[$i]}_k_${k[$i]}
	
	## Move to new directory
	cd run_m22_${m22[$i]}_m33_${m33[$i]}_m23_${m23[$i]}_k_${k[$i]}

	## Making the min and max for compositions for using in MOOSE input file
    crmin=$(echo $cr - $tol | bc)
    crmax=$(echo $cr + $tol | bc)
    comin=$(echo $co - $tol | bc)
	comax=$(echo $co + $tol | bc)
	
	## substitute the compositions in MOOSE input file
	sed "s/TTT/$temp/g;s/crmin/$crmin/g;s/crmax/$crmax/g;s/comin/$comin/g;s/comax/$comax/g;s/m22/${m22[$i]}/g;s/m23/${m23[$i]}/g;s/m33/${m33[$i]}/g;s/k0/${k[$i]}/g" <../FeCrCo.i >FeCrCo_m22_${m22[$i]}_m33_${m33[$i]}_m23_${m23[$i]}_k_${k[$i]}.i

	## substitute the input and application file in slurm
    sed "s/FeCrCo.i/FeCrCo_m22_${m22[$i]}_m33_${m33[$i]}_m23_${m23[$i]}_k_${k[$i]}.i/g;s/SAMPLE_JOB/SD_$i/g" <../slurm-batch.bash>slurm-batch.bash

	## submit job to cluster
    sbatch slurm-batch.bash
	
	## return to previous directory
    cd ..
done ##end i loop
