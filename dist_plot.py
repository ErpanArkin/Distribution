def parse_files(files_filename,nodes_filename):
    '''
    parse files and nodes using pandas DataFrame. Additional 'notAllocated' and 
    'AssignedNode' columns are added in files to indicate state of each file and the node it has assigned to.
    '''
    import pandas as pd
    import numpy as np
    files = pd.read_csv(files_filename,sep=' ',header=None,comment='#')
    nodes = pd.read_csv(nodes_filename,sep=' ',header=None,comment='#')
    files['notAllocated'] = True
    files['AssignedNode'] = ''
    nodes['files'] = ''
    nodes['files'] = nodes['files'].apply(list)
    nodes[2]=nodes[1] #make a copy of the total capacity
    return files,nodes


def distribute(files,nodes):

    '''
    Sort the files and the nodes by size and capacity. Assign the biggest file 
    to the nodes with largest avialible capacity. Reduce the capacity by the 
    size of the file it is assigned. If the largest files size is bigger
    than the largest available node capacity, Mark as NULL. Repeat until all 
    files are allocated or marked as NULL. 
    '''
    files.sort_values(1,inplace=True,ascending=False)
    while any(files['notAllocated']):
        frest = files[files['notAllocated']].copy()
        nodes.sort_values(1,inplace=True,ascending=False)
        for i in range(min(sum(frest['notAllocated']),len(nodes[1]))):
            if nodes[1].iloc[i] >= frest[1].iloc[i]:
                nodes.set_value(nodes.index[i],1,nodes[1].iloc[i] - frest[1].iloc[i])
                files.set_value(frest.index[i],'notAllocated',False)
                files.set_value(frest.index[i],'AssignedNode',nodes[0].iloc[i])
                nodes['files'].iloc[i].append(frest[0].iloc[i])
            elif i == 0:
                files.set_value(frest.index[i],'notAllocated',False)
                files.set_value(frest.index[i],'AssignedNode','NULL')

def plot_bar(files,nodes):
    '''
    plot the usage of each node containing blocks of bar for the files the node has been assigned.
    '''
    import matplotlib.pyplot as plt
    import pandas as pd
    files_nodes = pd.pivot_table(files[files['AssignedNode'] != 'NULL'], values=[1], index='AssignedNode', columns=[0])
    nodes.set_index(0,inplace=True)
    nodes.columns = ['left','files','total']
    total_fn = pd.concat([files_nodes,nodes['left']],axis=1)
    ax = total_fn.plot.bar(stacked=True,title='Files distribution amoung nodes')
    ax.set_xlabel("Nodes");ax.set_ylabel("Capacity")
    ax.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.2)
    plt.tight_layout(rect=(0,0,0.7,1))
    plt.show()

def print_output(files,nodes,out):
    from tabulate import tabulate
    nodes.index.name = 'Nodes'
    print tabulate(nodes, headers='keys', tablefmt='fancy_grid')	
    if out:
        files.to_csv('files.out',columns=[0,'AssignedNode'],header=False,sep=' ',index=False)
        nodes.to_csv('nodes.out',header=False,sep=' ',index=False)
    

