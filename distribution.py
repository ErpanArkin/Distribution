from argparse import ArgumentParser
from optparse import OptionParser
from dist_plot import *


description = "Distribute a list of files with different sizes to a list of nodes with different capacities"

parser = OptionParser(description=description)
parser.add_option("-f", "--files",help="filename of a list of files with sizes separated by space",
                  action="store", type="string", default="nodes", dest="files_filename")
parser.add_option("-n", "--nodes",help="filename of a list of nodes with capacities separated by space",
                  action="store", type="string", default="nodes", dest="nodes_filename")
parser.add_option("-o", "--output",help="output the results to files",
                  action="store_true",  default=False, dest="out_files")
parser.add_option("-p", "--plot",help="plot nodes usage",
                  action="store_true",  default=False, dest="plot_dist")
(options, args) = parser.parse_args()
if options.files_filename is None or options.nodes_filename is None:   # if filename is not given
    parser.error('Check if all the file names are given!')

files, nodes = parse_files(options.files_filename,options.nodes_filename)

distribute(files,nodes)

if options.plot_dist:
    plot_bar(files,nodes)

print_output(files,nodes,options.out_files)
