import argparse
from lib.filesdistributor import FilesDistributor

description = "Distribute a list of files with different sizes to a list of nodes with different capacities"

parser = argparse.ArgumentParser(description=description)
parser.add_argument("-f", "--files", help="file name of a list of files with sizes separated by space",
                  action="store", type=str, default=None, dest="files_filename", required=True)
parser.add_argument("-n", "--nodes", help="file name of a list of nodes with capacities separated by space",
                  action="store", type=str, default=None, dest="nodes_filename",required=True)
parser.add_argument("-o", "--output", help="output file name, if not given, output to stdout",
                  action="store", type=str, default=None, dest="output_filename")
parser.add_argument("-p", "--plot", help="plot nodes usage",
                  action="store_true", default=False, dest="plot_dist")
args = parser.parse_args()

distribute = FilesDistributor(args.files_filename, args.nodes_filename)

distribute.distribute()

distribute.print_output(args.output_filename)

if args.plot_dist:
    distribute.plot_bar()
