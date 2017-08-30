import pandas as pd
import numpy as np


class FilesDistributor:
    def __init__(self, files_filename, nodes_filename):
        """
        Distribute a list of files with different sizes to a list of nodes with different capacities
        """
        self.parse_files(files_filename, nodes_filename)
        if self.nodes.empty or self.files.empty:
            raise RuntimeError("one of the file contents is empty")

    def parse_files(self, files_filename, nodes_filename):
        """
        parse files and nodes using pandas' DataFrame.
        Adding 'notAllocated' and 'AssignedNode' columns in files to indicate the state of each file
        and the node it has assigned to. Adding 'files' columns to indicate a list of files it has
        been assigned to.
        """
        # read two files as pandas Dataframes
        files = pd.read_csv(files_filename, sep=' ',
                            header=None, comment='#', names=['files', 'size'],
                            dtype={'files': str, 'size': np.int32})
        nodes = pd.read_csv(nodes_filename, sep=' ',
                            header=None, comment='#', names=['nodes', 'capacity'],
                            dtype={'nodes': str, 'capacity': np.int32})
        # initialize them
        files['notAllocated'] = True
        files['AssignedNode'] = ''
        nodes['files'] = ''
        nodes['files'] = nodes['files'].apply(list)
        # make a copy of the total capacity
        nodes['space_left'] = nodes['capacity']
        self.files = files
        self.nodes = nodes

    def distribute(self):
        """
        First, sort the files and the nodes by size and capacity respectively. Then, assign the biggest file
        to the nodes with largest available capacity. Then, reduce the capacity by the
        size of the file it was assigned. If the largest file size is bigger
        than the largest available node capacity, Mark as NULL. Repeat until all
        files have been allocated or marked as NULL.
        """
        files = self.files
        nodes = self.nodes
        files.sort_values('size', inplace=True, ascending=False)
        while any(files['notAllocated']):  # repeat if any of the files is not allocated.
            rest_files = files[files['notAllocated']].copy()
            rest_files.sort_values('size', inplace=True, ascending=False)
            nodes.sort_values('space_left', inplace=True, ascending=False)  # sort the nodes by capacity
            for i in range(min(sum(rest_files['notAllocated']), len(nodes['space_left']))):
                # iterate for the shorter of two lists
                if nodes['space_left'].iloc[i] >= rest_files['size'].iloc[i]:  # if there is enough available space
                    # reduce the available space by file size
                    nodes.set_value(nodes.index[i], 'space_left',
                                    nodes['space_left'].iloc[i] - rest_files['size'].iloc[i])
                    # mark it as allocated
                    files.set_value(rest_files.index[i], 'notAllocated', False)
                    # mark which node it was assigned to
                    files.set_value(rest_files.index[i], 'AssignedNode', nodes['nodes'].iloc[i])
                    # append which file is assigned to this node
                    nodes['files'].iloc[i].append(rest_files['files'].iloc[i])
                elif i == 0:  # if there isn't available space on the largest node, mark it as NULL
                    files.set_value(rest_files.index[i], 'notAllocated', False)
                    files.set_value(rest_files.index[i], 'AssignedNode', 'NULL')
                    break  # break to resort the node, and repeat.

    def plot_bar(self):
        """
        plot the usage of each node containing blocks of bars for the files a node has been assigned.
        """
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches

        fig, ax = plt.subplots(1, 1)

        # pivot table: files vs nodes with file size as elements
        files_nodes = pd.pivot_table(self.files[self.files['AssignedNode'] != 'NULL'], values='size',
                                     index='AssignedNode', columns='files')

        # append space left on each node
        total_fn = pd.concat([files_nodes, self.nodes['space_left']], axis=1)

        # make stacked bar plot
        total_fn.plot.bar(ax=ax, stacked=True, title='Files distribution among nodes',
                          cmap='nipy_spectral_r', legend=False)
        ax.set_xlabel("Nodes")
        ax.set_ylabel("Capacity")

        black_patch = mpatches.Patch(color='black', label='space left')
        plt.legend(handles=[black_patch])

        plt.tight_layout()
        # to save the figure
        # plt.savefig('dist.png')
        plt.show()

    def print_output(self, out_files):
        from tabulate import tabulate
        # sort all by the node names
        self.files.set_index('files', inplace=True)
        self.files.sort_values('AssignedNode', inplace=True)
        self.nodes.set_index('nodes', inplace=True)
        self.nodes.sort_index(inplace=True)

        if out_files:
            # output files
            self.files.to_csv(out_files, columns=['AssignedNode'], header=False, sep=' ')
            # output nodes
            # self.nodes.to_csv('nodes.out',header=False,sep=' ',index=False)
        else:
            print tabulate(self.files[['size', 'AssignedNode']], headers='keys', tablefmt='fancy_grid')
            print tabulate(self.nodes, headers='keys', tablefmt='fancy_grid')
