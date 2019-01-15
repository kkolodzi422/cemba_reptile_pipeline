"""
Generates bed files for each cluster

Written by Wayne Doyle
"""
import pandas as pd
import numpy as np
import subprocess

# Get atac clusters
cluster_information = pd.read_table('/cndd/kkolodzi/REPTILE/MOp/cluster_info/cell_info.tsv',
                                    sep = '\t', header = 0, index_col = 0)
atac_idx = cluster_information.index.str.contains('^[A-Z]*_CEMBA.*$')
cluster_information = cluster_information.loc[atac_idx]
unq_clusts = cluster_information['cluster_ID'].unique()

# Write bed files
    
dir_atac = '/cndd/projects/Public_Datasets/CEMBA/snATACSeq/Datasets'
for cluster in unq_clusts:
    # Get cell information
    rel_cells = cluster_information.loc[cluster_information['cluster_ID'] == cluster]
    #split_info = pd.DataFrame(rel_cells.index.str.split('([A-Z]+)_(CEMBA\d\w+)').tolist())
    split_info = pd.DataFrame(rel_cells.index.str.split('([A-Z]+)_(CEMBA)').tolist())
    split_info[3]='CEMBA'+split_info[3].astype(str)
    split_info= split_info.drop(split_info.columns[2],axis=1)
    split_info = split_info.replace('',np.nan).dropna(axis = 'columns',how = 'all')
    split_info.columns = ['barcode','sample_tmp']
    split_name = split_info['sample_tmp'].str.split('_',expand = True)
    split_name.columns = ['C','slice','date']
    tmp = pd.DataFrame(index=range(split_name.shape[0]),columns= ['sample'])

    for row in split_name.itertuples():
    	index = row.Index
    	if row.date == '171206' or row.date == '171212': 
        	rep = 'rep1'
    	elif row.date == '171207' or row.date == '171213':
        	rep = 'rep2'
    	elif row.date == '180104':
        	rep = 'rep3'
    	else:
        	raise ValueError('date unexpected')
    	name = row.C + row.date + '_' + row.slice + '_' + rep
    	tmp['sample'].loc[index] = name

    split_info['sample']=tmp['sample']

   # Generate file
    fn_out = '{}.bed'.format(cluster)
    open(fn_out,'w').close()
    unq_samps = split_info['sample'].unique()
    for sample in unq_samps:
        x = sample.split('_')[1]
        rel_sample = split_info['barcode'].loc[split_info['sample'] == sample]
        fn_tmp = 'tmp_clust_ids.tsv'
        rel_sample.to_csv(fn_tmp,sep = '\t', index=False,header=False)
        fn_re = '{0}/{2}/{1}/readends/{1}.readends.bed.gz'.format(dir_atac,sample,x)
        sh_args = ['zcat',fn_re, '|', 'awk', 'NR==FNR {a[$1] = 1}; NR > FNR {if (a[$4]) {print}}', fn_tmp]
        fout = open(fn_out,'a')
        proc = subprocess.call(sh_args,stdout=fout)
        fout.close()



print('all done')

