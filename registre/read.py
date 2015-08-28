import json

def read_registre(filename):
    with open(filename) as file:
        for line in file.readlines():
            yield json.loads(line)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser("Extract activity records from Tableau logs.")
    parser.add_argument("-i", "--input",
                        help="path to the log file to parse")

    args = parser.parse_args()
    if args.input is None:
        raise RuntimeError("You must provide an input file.")
        parser.print_help()

    read_registre(args.input) 
