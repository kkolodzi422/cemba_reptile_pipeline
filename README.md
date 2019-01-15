Run REPTILE to call enhancers from CEMBA snATAC and snmC-seq data

Requires integrated cluster analysis (individual cell assignments) for methylation and ATAC data
Necessary inputs:

-Trainig data:
	-mESC_ATAC.bw
	-mESC_Meth.bw
-BigWig files at integrated cluster level for ATAC and methylation 
-DMRs called for all integrated clusters (format file: choose DMRs that are 3DMS and format: chr, start, end, dmr_#)
-Cell cluster assignments (cell info file, cellID and clusterID, ATAC and methylation)  
-Data info file:
	path to bigwig files for atac, methylation, training 
-Genome window  bed file, 2kb window sliding 100bp,  mm10_w2kb_s100bp.bed 

Initial steps:

1. Obtain integrated clustering
2. Call DMRs for integrated clusters
3. Generate BigWig files
	a. methylation: allc2bigwig (requires mm.10.fasta with chrM)  
	b. atac: gen_atac_bed, sort_beds, bed_to_bigwig

REPTILE steps:


1. run_reptile.sh  
	a. preprocess (preprocess.py)
	b. train (train.R)
	c. predict (preprocess.py)

2. run_reptile_2.sh (loop for each cluster) 
	a. score (compute_score.R)
	b. enhancers (call_enhancer.py) 
