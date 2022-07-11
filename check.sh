#!/bin/bash

dirs=($(find . -name "run_m*"))

count=0
total=0

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
            line="$(grep "dt =" $logfile | tail -1)"
 
	    echo $item, $line
	    
            echo "$item, $line" >> ../status.txt
	fi 
   fi

    total=$(($total+1))

    cd ..
done
echo "---" >> status.txt
echo $count out of $total completed

#echo "scale=2 ; $count / $total" | bc