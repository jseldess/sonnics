"""TBD

Help: python3 sonnics.py --help

Example usage:

    Generate poem with 14 lines in couplets:
        python3 sonnics.py -m 14 -sz "couplets"
    Generate poem with 14 lines in Petrarchan stanzaic form:
        python3 sonnics.py -m 14 -sz "petrarchan"
    Generate poem with 14 lines in Elizabethan stanzaic form:
        python3 sonnics.py -m 14 -sz "elizabethan"
    Generate poem with 14 lines, random stanza breaks:
        python3 sonnics.py -m 14 -sz "random"
    Generate poem with 14 lines, no stanza breaks:
        python3 sonnics.py -m 14 -sz "none"
    Generate poem with 14 lines in couplets, 2 removed
    from lines at random:
        python3 sonnics.py -m 14 -sz "couplets" -r 2

"""

import argparse
import os
import re
import random
from time import gmtime, strftime

parser = argparse.ArgumentParser(
    description="""TBD""")
parser.add_argument("-s", "--source_file",
                    help="Source text file (default: source.txt).",
                    default="source.txt")
parser.add_argument("-d", "--new_file_dir",
                    help="""Path to the directory where the new file
                    will be created (default: generated_files).""",
                    default="generated_files")
parser.add_argument("-m", "--max_lines", type=int,
                    help="Max number of lines of text in total.")
parser.add_argument("-sz", "--stanzas", choices=["couplets", "random", "petrarchan", "elizabethan", "none"],
                    help="""Stanzaic form. Either couplets with one empty
                    line between, random with 0-4 empty lines between, or no
                    stanza breaks (default: couplets).""",
                    default=["couplets"])
parser.add_argument("-r", "--remove_words", type=int,
                    help="""Number of words to remove from the start
                    of a line.""")

args = parser.parse_args()

# Create a new directory for generated files, if it doesn't exist.
if not os.path.exists(args.new_file_dir):
    os.makedirs(args.new_file_dir)

# Create a new file named with the current timestamp and flags passed.
filename = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
if args.max_lines:
    filename += "_maxlines" + str(args.max_lines)
if args.remove_words:
    filename += "_removewords"
if args.stanzas == "couplets":
    filename += "_couplets"
if args.stanzas == "petrarchan":
    filename += "_petrarchan"
if args.stanzas == "elizabethan":
    filename += "_elizabethan"
if args.stanzas == "random":
    filename += "_random"
filename += "_py.txt"
new_file = open(os.path.join(args.new_file_dir, filename), "a")

# Read source file and store its lines as a list of strings in source.
with open(args.source_file) as file:
    source = file.readlines()
    lines_seen = set()
    total_lines = 0
    trimmed = 0
    while len(source) > 0:
        # If --max_lines is passed, break out of the loop
        # as soon as the max lines have been written.
        if args.max_lines:
            if total_lines == args.max_lines:
                break
        line = random.choice(source)
        source.remove(line)
        if not line.isspace():
            # At random, skip the line and continue the next iteration.
            if random.choice([0, 1]) == 1:
                print("Skip line")
                continue
            # If --remove_words is passed, remove the specified number
            # of words from the start of the line.
            if args.remove_words:
                remove_expr = "^" + ("\W*\w+" * args.remove_words) + "\W*"
                line = re.sub(remove_expr, "\n", line)
                trimmed = 1
                # If line already seen, continue the next iteration.
                if line in lines_seen:
                    continue
            # If line already seen, continue the next iteration.
            else:
                if line in lines_seen:
                    continue
            new_file.write(line.lstrip())
            lines_seen.add(line)
            if trimmed == 1:
                print("Write line, trimmed")
            else:
                print("Write line")
            total_lines += 1
            trimmed = 0
            # Define the stanzaic form.
            if args.stanzas == "couplets":
                if (total_lines % 2) == 0:
                    new_file.write("\n")
            if args.stanzas == "petrarchan":
                if total_lines == 8:
                    new_file.write("\n")
            if args.stanzas == "elizabethan":
                if total_lines == 4:
                    new_file.write("\n")
                if total_lines == 8:
                    new_file.write("\n")
                if total_lines == 12:
                    new_file.write("\n")
            if args.stanzas == "random":
                if random.choice([0, 1]) == 1:
                    new_file.write(random.choice([
                    "", "", "", "", "\n", "\n\n", "\n\n\n", "\n\n\n\n"]))
            if args.stanzas == "none":
                continue

# print(lines_seen)
print("File {} created".format(filename))
print("Total lines: {}".format(total_lines))
