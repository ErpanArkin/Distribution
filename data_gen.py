import argparse
import random
import string
import numpy as np

description = "Generate a list of strings and integers."

parser = argparse.ArgumentParser(description=description)
parser.add_argument("-s", "--sizes", help="three arguments in the order of number of data, "
                                          "lower and higher bound of the sizes", required=True, nargs=3)
parser.add_argument("-o", "--output", help="output file name",
                    action="store", type=str, required=True, dest="output_filename")

args = parser.parse_args()


def randomword(length):
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(length))


with open(args.output_filename, 'w') as f:
    for i in range(int(args.sizes[0])):
        f.write("{} {}\n".format(randomword(5), np.random.randint(int(args.sizes[1]), high=int(args.sizes[2]))))
