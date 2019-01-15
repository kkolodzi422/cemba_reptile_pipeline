for file in cluster_*.srt.bed; do
	echo $file 
	bedtools genomecov -bg -i $file -g /cndd/kkolodzi/REPTILE/tmp/mm10.genome | head -n 1000 > ${file}.bg
	echo "converting"
	/cndd/bin/bedGraphToBigWig ${file}.bg /cndd/kkolodzi/REPTILE/tmp/mm10.genome ${file}.bw
done
echo "done" 

