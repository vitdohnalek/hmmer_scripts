#Write fasta file from hmmer results for a single results file
from Bio import SeqIO
import argparse
import os


def parse_arguments():
    parser = argparse.ArgumentParser(description="get results of hmmer search and writes them in fasta file")
    parser.add_argument(
        "--results",
        type=str,
        required=True,
        help="Path to the output result file."
    )
    parser.add_argument(
        "--db",
        type=str,
        required=True,
        help="Path to the db FASTA file."
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
	get_results(results=args.results,db=args.db,output_dir=args.output_dir)

if __name__ == "__main__":
	main()
