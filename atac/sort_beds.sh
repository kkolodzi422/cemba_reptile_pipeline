#!/bin/bash
#
# Sortes bed files by chromosome and start position
#
# Written by Wayne Doyle

shopt -s nullglob

for file in cluster_*.bed; do
    echo "Processing $file"
    sort -k1,1V -k2,2n $file > ${file}.srt.bed
done

echo 'all done'
