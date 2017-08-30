from optparse import OptionParser
import sys
from filesdistributor import FilesDistributor

description = "Distribute a list of files with different sizes to a list of nodes with different capacities"

parser = OptionParser(description=description)
parser.add_option("-f", "--files", help="file name of a list of files with sizes separated by space",
                  action="store", type="string", default=None, dest="files_filename")
parser.add_option("-n", "--nodes", help="file name of a list of nodes with capacities separated by space",
                  action="store", type="string", default=None, dest="nodes_filename")
parser.add_option("-o", "--output", help="output file name, if not given, output to stdout",
                  action="store", type="string", default=None, dest="out_files")
parser.add_option("-p", "--plot", help="plot nodes usage",
                  action="store_true", default=False, dest="plot_dist")
(options, args) = parser.parse_args()


if not options.files_filename or not options.nodes_filename:  # if filename is not given
    # parser.print_help()
    parser.error('Check if all the file names are given! {}'.format(parser.print_help()))

distribute = FilesDistributor(options.files_filename, options.nodes_filename)

distribute.distribute()

if options.plot_dist:
    distribute.plot_bar()

distribute.print_output(options.out_files)
