wget "http://www.rcsb.org/pdb/download/downloadFile.do?fileFormat=FASTA&compression=NO&structureId=${@}" -O "${@}.fasta"
psiblast -db nr/nr  -evalue 0.001 -query ${@}.fasta -out_ascii_pssm ${@}_pssm.txt -out ${@}.psiblast.output -num_iterations 3 -comp_based_stats 0 -num_threads 8
