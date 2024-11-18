from Bio import SeqIO
import argparse
import glob
import os


def parse_arguments():
    parser = argparse.ArgumentParser(description="get results of hmmer search and writes them in fasta file")
    parser.add_argument(
        "--results",
        type=str,
        required=True,
        help="Path to the output results directory."
    )
    parser.add_argument(
        "--db",
        type=str,
        required=True,
        help="Path to the output dbs directory."
    )
    #Optional output path argument
    parser.add_argument(
    	"--output_dir",
    	type=str,
    	default="./",
    	help="Path to output directory. Default is current directory."
    	)
    return parser.parse_args()

def get_results(results: str, db: str, output_dir: str = "./") -> None:
	
	fasta = ""
	if not output_dir.endswith("/"):
		output_dir += "/"

	#Prepare output path from results file
	_, file_name = os.path.split(results)
	base_name = os.path.splitext(file_name)[0]
	output_name = f"{base_name}.hmmer.fasta"
	output_file_path = os.path.join(output_dir, output_name)

	#Collect results IDs
	IDs = set()
	with open(results, "r") as f:
		for l in f:
			if l.startswith(">>"):
				IDs.add(l.split()[1])

	#Collect fastas corresponding to results IDs
	for seq_rec in SeqIO.parse(db, "fasta"):
		if seq_rec.id in IDs:
			fasta += f">{seq_rec.description}\n{seq_rec.seq}\n"

	with open(output_file_path, "w") as f:
		f.write(fasta)

def main():
	args = parse_arguments()
	db_datasets = []
	results_datasets = []

	if not args.db.endswith("/"):
		args.db += "/"
	if not args.results.endswith("/"):
		args.results += "/"

	#Get directories for results and dbs
	db_directory,_ = os.path.split(args.db)
	results_directory,_ = os.path.split(args.results)

	#Get datasets for dbs and results
	for file in glob.glob(f"{args.db}*"):
		_, file_name = os.path.split(file)
		base_name = os.path.splitext(file_name)[0]
		db_datasets.append(base_name)
	for file in glob.glob(f"{args.results}*"):
		_, file_name = os.path.split(file)
		base_name = os.path.splitext(file_name)[0]
		results_datasets.append(base_name)

	#If dataset in both dbs and results run the get_results, else give Warning
	for dataset in db_datasets:
		if dataset in results_datasets:
			get_results(results=f"{results_directory}/{dataset}.res",db=f"{db_directory}/{dataset}.fasta",output_dir=args.output_dir)
		else:
			print(f"WARNING: {dataset} does not have corresponding result file")
	for dataset in results_datasets:
		if not dataset in db_datasets:
			print(f"WARNING: {dataset} results does not have corresponding db file")

if __name__ == "__main__":
	main()
