class files_distributor:

   def __init__(self,files_filename,nodes_filename):
       self.files,  self.nodes = self.parse_files(files_filename,nodes_filename)


   def parse_files(self,files_filename,nodes_filename):
       '''
       parse files and nodes using pandas DataFrame. 
       Adding 'notAllocated' and 'AssignedNode' columns in files to indicate state of each file and the node it has assigned to.
       Adding 'files' columns to indicate a list of files it has been assigned to.
       '''
       import pandas as pd
       import numpy as np
       #read two files as pandas Dataframes
       files = pd.read_csv(files_filename,sep=' ',\
           header=None,comment='#',names=['files','size'],\
           dtype={'files':str,'size':np.int32})
       nodes = pd.read_csv(nodes_filename,sep=' ',\
           header=None,comment='#',names=['nodes','capacity'],\
           dtype={'files':str,'size':np.int32})
       #initialize them with 
       files['notAllocated'] = True
       files['AssignedNode'] = ''
       nodes['files'] = ''
       nodes['files'] = nodes['files'].apply(list)
       #make a copy of the total capacity
       nodes['space_left']=nodes['capacity']
       return files,nodes


   def distribute(self):

       '''
       Sort the files and the nodes by size and capacity respectively. First, assign the biggest file 
       to the nodes with largest avialible capacity. Then, reduce the capacity by the 
       size of the file it has been assigned. If the largest files size is bigger
       than the largest available node capacity, Mark as NULL. Repeat until all 
       files are allocated or marked as NULL. 
       '''
       files = self.files.copy()
       nodes = self.nodes.copy()
       files.sort_values('size',inplace=True,ascending=False)
       while any(files['notAllocated']): #repeat if any of the files is not allocated.
           frest = files[files['notAllocated']].copy()
           nodes.sort_values('space_left',inplace=True,ascending=False) #sort the nodes by capacity
           for i in range(min(sum(frest['notAllocated']),len(nodes['space_left']))): #for the shorter of two lists
               if nodes['space_left'].iloc[i] >= frest['size'].iloc[i]: #if there is enough available space
                   #reduce the available sapce by file size
                   nodes.set_value(nodes.index[i],'space_left',nodes['space_left'].iloc[i] - frest['size'].iloc[i])
                   #mark it as allocated
                   files.set_value(frest.index[i],'notAllocated',False)
                   #mark which node it was assigned to
                   files.set_value(frest.index[i],'AssignedNode',nodes['nodes'].iloc[i])
                   #append which file is assigned to this node
                   nodes['files'].iloc[i].append(frest['files'].iloc[i])
               elif i == 0: # if there isn't available space on the largest node, mark it as NULL
                   files.set_value(frest.index[i],'notAllocated',False)
                   files.set_value(frest.index[i],'AssignedNode','NULL')
                   break #break to resort the node, and repeat.
       self.files_done = files.copy()
       self.nodes_done = nodes.copy()

   def plot_bar(self):
       '''
       plot the usage of each node containing blocks of bar for the files the node has been assigned.
       '''
       import matplotlib.pyplot as plt
       import pandas as pd
       #pivot table files vs nodes with file size as elements
       files_nodes = pd.pivot_table(self.files_done[self.files_done['AssignedNode'] != 'NULL'], values='size', index='AssignedNode', columns='files')
       self.nodes_done.set_index('nodes',inplace=True)
       #append space left on each node
       total_fn = pd.concat([files_nodes,self.nodes_done['space_left']],axis=1)
       #make stacked bar plot
       ax = total_fn.plot.bar(stacked=True,title='Files distribution among nodes',cmap='nipy_spectral_r')
       ax.set_xlabel("Nodes");ax.set_ylabel("Capacity")
       #make legend for the file names, ncol will increase accordingly with the number of files
       ax.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.2,ncol=int((len(self.files_done['files'])+14)/14))
       plt.tight_layout(rect=(0,0,0.7,1))
       plt.show()

   def print_output(self,out_files):
       from tabulate import tabulate
       self.files_done.set_index('files',inplace=True)    
       self.nodes_done.sort_values('capacity',inplace=True,ascending=False)	

       if out_files:
           #output files
           self.files_done.to_csv(out_files,columns=['AssignedNode'],header=False,sep=' ')
           #output nodes
           #self.nodes_done.to_csv('nodes.out',header=False,sep=' ',index=False)
       else:
           print tabulate(self.files_done[['size','AssignedNode']], headers='keys', tablefmt='fancy_grid')
           #print tabulate(self.nodes_done, headers='keys', tablefmt='fancy_grid')

       

