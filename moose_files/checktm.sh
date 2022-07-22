#!/bin/bash
# This file is the same as "check.sh", but it work for MOOSE jobs that have a shortened name (such as
# the jobs where both thermodynamics and kinetic parameters are being changed)
dirs=($(find . -name "run_[0-9]*"))

count=0
total=0
failed=0

touch status.txt
date >> status.txt
for item in ${dirs[*]}
do    
    cd $item

    exfile=($(find . -name "FeCrCo*_exodus*"))

    if test -f "$exfile"; 
    then
       	count=$(($count+1))
    else
        logfile=($(find . -name "log_*"))
        if test -f "$logfile"
        then
            if grep -q "terminated" "$logfile"
            then
                failed=$(($failed+1))
                echo $item, failed 
            else   
                line="$(grep "dt =" $logfile | tail -1)"
                if [[ $line == *"dt"* ]]
                then
                    echo $item, $line
                    echo "$item, $line" >> ../status.txt
                else
                    failed=$(($failed+1))
                    echo $item, failed 
                fi
            fi
        fi 
    fi

    total=$(($total+1))

    cd ..
done
echo "---" >> status.txt
echo $count out of $total completed, $failed failed

#echo "scale=2 ; $count / $total" | bc
