#!/bin/bash

OLDIFS=$IFS # save original IFS setting
IFS=','

## reading data from CSV file
while read -r a b c d e f g h; do
	lr+=("$a")
	ep+=("$b")
	bs+=("$c")
	size+=("$d")
	dc+=("$e")
	f1+=("$f")
	f2+=("$g")
	f3+=("$h")
done < input_data.csv
IFS=$OLDIFS # restore orig setting

## For loop for running all the jobs over super computer (R2 or Borah)

for i in {0..5} ##all rows ${#cr[*]} 
do
	## Make a directory for new job with its name
	mkdir run_"$i"_f_${f1[$i]}_${f2[$i]}_${f3[$i]}_lr_${lr[$i]}_ep_${ep[$i]}_bs_${bs[$i]}_size_${size[$i]}_dc_${dc[$i]}
	
	## Copy all the required files to new directory
	cp -R input_data.csv ./run_"$i"_f_${f1[$i]}_${f2[$i]}_${f3[$i]}_lr_${lr[$i]}_ep_${ep[$i]}_bs_${bs[$i]}_size_${size[$i]}_dc_${dc[$i]}
	
	## Move to new directory
	cd run_"$i"_f_${f1[$i]}_${f2[$i]}_${f3[$i]}_lr_${lr[$i]}_ep_${ep[$i]}_bs_${bs[$i]}_size_${size[$i]}_dc_${dc[$i]}
	
	## substitute the compositions in MOOSE input file
	pyfile=ml_"$i"_f_${f1[$i]}_${f2[$i]}_${f3[$i]}_lr_${lr[$i]}_ep_${ep[$i]}_bs_${bs[$i]}_size_${size[$i]}_dc_${dc[$i]}.py

	sed "s/f1_/${f1[$i]}/g;s/f2_/${f2[$i]}/g;s/f3_/${f3[$i]}/g;s/lr_/${lr[$i]}/g;s/ep_/${ep[$i]}/g;s/bs_/${bs[$i]}/g;s/size_/${size[$i]}/g;s/dc_/${dc[$i]}/g;" <../microstructure_model.py >$pyfile

	## substitute the input and application file in slurm
    sed "s/microstructure_model.py/$pyfile/g;s/SAMPLE_JOB/ML_$i/g" <../slurm-batch-gpu.bash>slurm-batch-gpu.bash

	## submit job to cluster
    sbatch slurm-batch-gpu.bash
	
	## return to previous directory
    cd ..
done ##end i loop
