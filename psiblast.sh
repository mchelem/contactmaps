wget "http://www.rcsb.org/pdb/download/downloadFile.do?fileFormat=FASTA&compression=NO&structureId=${@}" -O "${@}.fasta"
psiblast -db blastdb/pdbseqres -out_pssm ${@}.ckp -evalue 0.01 -query ${@}.fasta -out_ascii_pssm ${@}_pssm.txt -out output_file -num_iterations 3
