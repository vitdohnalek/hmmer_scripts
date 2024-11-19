## Multiple Sequence Alignment

For larger alignments you can set multiple cores with --nt {NUMBER}, or use mafft {FASTA_FILE} > {FILE_NAME}.fasta

```bash
mafft --maxiterate 1000 --localpair {FASTA_FILE} > {FILE_NAME}.fasta
```

## HMM Profile generation

```bash
hmmbuild {FILE_NAME}.hmm {ALIGNMENT_FILE}
```

## Hmmer Search

Adjust E value threshold as needed. The lower the value, the more stringent the search will be.

Against single dataset: 
```bash
hmmsearch -E 0.001 {HMM_FILE} {FASTA_FILE} > {FILE_NAME}.res
```

With multiple datasets:
```bash
for i in ./{FASTA_FILE_DIRECTORY}/*.fasta
do
hmmsearch -E 0.001 {HMM_FILE} $i > $(basename $i .fasta).res
done
```

You can set the output directory by modifying the command:
```bash
for i in ./{FASTA_FILE_DIRECTORY}/*.fasta
do
hmmsearch -E 0.001 {HMM_FILE} $i > ./{OUTPUT_DIRECTORY}/$(basename $i .fasta).res
done
```


## Converting Hmmer Results Into New Fasta

```bash
source myenv/bin/activate
python3  get_hmmer_results_batch.py --db {FASTA_FILES_DIRECTORY} --results {RESULTS_FILES_DIRECTORY} --output_dir {OUTPUT_FASTA_FILES_DIRESTORY}
deactivate
```

## Merging Files

If you want to merge all the generated hmmer.fasta files into a single file, use cat command:
```bash
cat *.hmmer.fasta > {FILE_NAME}.fasta
```