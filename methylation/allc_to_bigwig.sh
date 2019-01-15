#!/bin/bash
# NOTE: We added chrM to the fasta file

ls allc*.gz | xargs --max-procs=8 -I{} nohup methylpy allc-to-bigwig --allc-file {} --output-file {}.bw --ref-fasta ./mm10.fasta --mc-type CGN --bin-size 100
