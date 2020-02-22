#!/usr/bin/bash

DIR=Tests/$2
NUM_TIMES=`ls -1q ./$DIR/in* | wc -l | bc`

for((i = 1; i <= $NUM_TIMES ; ++i)); do
    echo $i
    diff -w <(./$1 < ./$DIR/in$i) ./$DIR/out$i || break
done
