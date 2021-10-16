"""TBD

Help: python3 first_word.py --help

Example usage:

    Extract lines starting with a given word, including duplicates:
        python3 first_word.py -w "<word>"
    Extract lines starting with a given word, excluding duplicates:
        python3 first_word.py -w "<word>" -u

"""

import argparse
import os
from time import gmtime, localtime, strftime

parser = argparse.ArgumentParser(
    description="""TBD""")
parser.add_argument("-w", "--first_word",
                    help="First word of line.")
parser.add_argument("-u", "--unique_lines",
                    action="store_true",
                    help="""Make sure each line matching line is unique
                    (default: False)""")
parser.add_argument("-s", "--source_file",
                    help="Source text file (default: source.txt).",
                    default="source.txt")
parser.add_argument("-d", "--new_file_dir",
                    help="""Path to the directory where the new file
                    will be created (default: generated_files/first_words).""",
                    default="generated_files/first_words")

args = parser.parse_args()

# Create a new directory for generated files, if it doesn't exist.
if not os.path.exists(args.new_file_dir):
    os.makedirs(args.new_file_dir)

# Create a new file named with the current timestamp and flags passed.
created_at = strftime("%Y-%m-%d-%H:%M:%S", localtime())
filename = created_at
filename += "_" + args.first_word
if args.unique_lines:
    filename += "_unique"
filename += "_py.txt"
new_file = open(os.path.join(args.new_file_dir, filename), "a")

# Read source file and store its lines as a list of strings in source.
with open(args.source_file) as file:
    source = file.readlines()
    lines_seen = set()
    total_lines = 0
    new_file.write(created_at + " ET\n\n\n")
    for line in source:
        if args.unique_lines:
            if line in lines_seen:
                continue
        if line.startswith(args.first_word):
            new_file.write(line.lstrip())
            total_lines += 1
            lines_seen.add(line)

print("File {} created".format(filename))
print("Total lines: {}".format(total_lines))
