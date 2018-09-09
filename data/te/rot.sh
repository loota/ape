#!/bin/bash
# Rotate an image 360 degrees 1 degree at a time and
# make an image for each degree
# Change the filename/filetype as appropriate
# Usage:
# rot.sh a0.bmp

if [ -z $1 ]
then
  echo "Usage:"
  echo "sh rot.sh a0.bmp"
  exit -1
fi
for x in `seq 1 360` ;
do
  convert -rotate $x $1 $x.bmp
done
