#!/bin/bash
LIMIT=20
LIMIT2=50
a=1
b=1

((a = 0))      # a=1
# Double parentheses permit space when setting a variable, as in C.

while (( a <= LIMIT ))   # Double parentheses, and no "$" preceding variables.
do
  echo "================================= $a ================================="
  while (( b <= LIMIT2 ))
  do
    python cc2420_channel_test.py -N $a -n 1000 2>/dev/null | grep Statistics
    ((b += 1))
  done
  ((a += 1))   # let "a+=1"

done
