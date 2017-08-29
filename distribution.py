from argparse import ArgumentParser
from optparse import OptionParser
from dist_plot import files_distributor


description = "Distribute a list of files with different sizes to a list of nodes with different capacities"

parser = OptionParser(description=description)
parser.add_option("-f", "--files",help="file name of a list of files with sizes separated by space",
                  action="store", type="string", default=None, dest="files_filename")
parser.add_option("-n", "--nodes",help="file name of a list of nodes with capacities separated by space",
                  action="store", type="string", default=None, dest="nodes_filename")
parser.add_option("-o", "--output",help="output file name, if not given, output to stdout",
                  action="store", type="string", default=None, dest="out_files")
parser.add_option("-p", "--plot",help="plot nodes usage",
                  action="store_true",  default=False, dest="plot_dist")
(options, args) = parser.parse_args()
if options.files_filename is None or options.nodes_filename is None:   # if filename is not given
    parser.error('Check if all the file names are given!')

# files, nodes = parse_files(options.files_filename,options.nodes_filename)

# distribute(files,nodes)

# if options.plot_dist:
#     plot_bar(files,nodes)

# print_output(files,nodes,options.out_files)

distribute = files_distributor(options.files_filename,options.nodes_filename)
distribute.distribute()
if options.plot_dist:
	distribute.plot_bar()
distribute.print_output(options.out_files)
