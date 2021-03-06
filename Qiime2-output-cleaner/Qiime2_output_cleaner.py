'''
taxonomy_arranger combines rows with the same taxa values and arrange them from greatest to smallest to prepare for truncating in top10searcher
'''
def taxonomy_arranger(input_file):
    #this part inserts the appropriate taxonomy assignment
    import re
    with open(input_file,'r') as file:
            f = file.read().split('\n')
            for ii in range(1,len(f)):
                f[ii] = re.split(',|\t',f[ii])
            replaced_output = f[1:len(f)]
            key = replaced_output[0][1:]
            header_row = replaced_output[0]
            sample_names = header_row[1:]
    import pandas as pd
    import numpy as np
    df = pd.read_csv(input_file, skiprows = 1, delimiter = "\t")
    df = df.values.tolist()
    df = pd.DataFrame(df)
    df_taxa = df[0]
    df = df.drop([0],axis=1) #get the columns with no taxa column
    df = df.astype(float).astype(int) #turn all the numbers to floats first then integers
    #generate sum of counts for all samples as a list
    total = []
    for ii in range(1,len(key)+1):
        total.append(df[ii].sum())
    df.insert(loc=0,column=0,value=df_taxa) #put the taxa column back
    df.columns= header_row #change the names of the columns to header_row
    #insert more taxa column so we can sort
    df_taxa = df['#OTU ID']
    for ii in range(1,len(df.columns)-1):
        label = '#OTU ID' + str(2*ii)
        df.insert(loc=2*ii,column=label,value=df_taxa)
    #get rid of the index column
    df.set_index('#OTU ID',inplace=False)
    #now we sort by abundance
    split_frames = []
    new_header = df.columns
    for ii in range(len(key)):
        split_frames.append(df.iloc[:,[ii*2,(2*ii)+1]].sort_values(by=new_header[(ii*2)+1], ascending=False))
    concatenated = split_frames[0].to_numpy()
    for ii in range(1,len(split_frames)): #now we merge them back to df with numpy array
        split_frames[ii] = split_frames[ii].to_numpy()
        concatenated = np.concatenate((concatenated,split_frames[ii]), axis = 1)
    header = df.columns.to_numpy()
    concatenated = np.vstack((header,concatenated))
    return(concatenated, header_row, sample_names, total)
'''
topsearcher seach for the top n number of taxa and truncate the data to that, the rest of the sequence values is combined to an "Others" row
input_array is the output from taxonomy_selector, output_file is where the output is saved to, header_row and total are things that are needed for plotting
top_taxa is how you specify how many top taxa to take from each sample (Warning: too many will result in gigantic legend unless you decrease font size)
'''
def topsearcher(input_array, top_taxa, total, sample_names):
    import numpy as np
    import pandas as pd
    all_sample = []
    for item in sample_names:
        all_sample.append([])
    f = input_array.tolist()
    f = list(filter(None,f)) #get rid of empty rows
    sample_length = int(len(f[0])/2)
    for line in f[1:]:
        i = 0
        for j in range(sample_length):
            line[2*j+1] = float(line[2*j+1])
            all_sample[i].append(line[2*j:2*j+2])
            i+=1
    # take second element for sort
    def takeSecond(elem):
        return elem[1]
    for i in range(sample_length):
        all_sample[i].sort(key=takeSecond,reverse=True)
    top_10 = []
    for i in range(sample_length):
        j = all_sample[i][0:top_taxa]
        for a in j:
            top_10.append(a[0])
    top_10 = list(set(top_10))
    #make an output list equal to number of samples
    output_list = []
    for ii in range(len(sample_names)):
        output_list.append([])
    m=0
    for i in all_sample:
        for j in i:
            if j[0] in top_10:
                output_list[m].append(j)
        m = m+1
    def takeFirst(elem):
        return elem[0]
    for i in range(sample_length):
        output_list[i].sort(key=takeFirst)
    #make list equal with length equal to number of taxa in output
    final = []
    for ii in range(len(top_10)):
        final.append([])
    top_10.sort()
    taxa_num = len(top_10)
    for i in range(taxa_num):
        final[i].append(top_10[i])
    for i in range(taxa_num):
        for j in output_list:
            for k in j:
                if final[i][0] == k[0]:
                    final[i].append(k[1])
    Taxon_assignment = []
    for line in final:
        line = line[0].split(';')
        line = [i for i in line if i]
        if len(line) != 0:
            length = len(line) - 1
            if "Subgroup" not in line[length]:
                if "uncultured" not in line[length] and "uncultivated" not in line[length] and line[length]!='__':
                    if "D_5__" in line[length] or "g " in line[length]:
                        ita_output = line[length].replace("D_5__", "g ")
                        ita_output = ita_output.split('g ')
                        ita_output[1] = ita_output[1].replace(" ","\ ")
                        ita_output[1] = "$\\it{"+ita_output[1]+"}$"
                        real_output = "g " + ita_output[1]
                        Taxon_assignment.append(real_output)
                    elif "D_6__" in line[length] or "s " in line[length]:
                        ita_output = line[length].replace("D_6__", "s ")
                        ita_output = ita_output.split('s ')
                        ita_output[1] = ita_output[1].replace(" ","\ ")
                        ita_output[1] = "$\\it{"+ita_output[1]+"}$"
                        real_output = "s " + ita_output[1]
                        Taxon_assignment.append(real_output)
                    else:
                        Taxon_assignment.append(line[length])
                else: #this means it contains "uncultured" or "uncultivated" or "__"
                    for ii in range(length+1):
                        if "uncultured" not in line[length-ii] and "uncultivated" not in line[length-ii] and "Subgroup" not in line[length-ii] and line[length-ii] != '__':
                            Taxon_assignment.append(line[length-ii])
                            break #exits for loop and move on to next line on csv   
                        elif "Subgroup" in line[length-ii]:    
                            for jj in range(length+1):
                                if "Subgroup" not in line[length-jj] and "uncultured" not in line[length-jj] and "uncultivated" not in line[length-jj] and line[length-jj] != '__':
                                    Taxon_assignment.append(line[length-jj] + " (" + line[length-ii] + ")")
                                    break
                                #else this moves on to next item on the list and checks again
                            break
                        # if none of those triggers, then "uncultured"/"uncultivated" is in there again
            else: #this means "Subgroup" is in the cell
                for ii in range(length+1):
                    if "Subgroup" not in line[length-ii] and "uncultured" not in line[length-ii] and "uncultivated" not in line[length-ii] and line[length-ii] != '__':
                        Taxon_assignment.append(line[length-ii] + " (" + line[length] + ")")
                        break
    output = []
    for item in Taxon_assignment:
        item = item.replace("D_0__", "d ")
        item = item.replace("D_1__", "p ")
        item = item.replace("D_2__", "c ")
        item = item.replace("D_3__", "o ")
        item = item.replace("D_4__", "f ")
        item = item.replace("D_5__", "g ")
        item = item.replace("D_6__", "s ")
        output.append(item)
    final = pd.DataFrame(final)
    final[0] = output
    final = final.values.tolist()
    #Generate "Others" row here
    init_array = np.array(final, dtype=object)
    num_array = np.delete(init_array,0,1).astype(float).astype(int)
    top_sum = num_array.sum(axis=0)
    others_array = total - top_sum
    others_array = others_array.astype(str)
    others_array = np.insert(others_array, 0, 'Others', axis=0)
    others_row = others_array.tolist()
    #append to final and output it
    final.append(others_row)
    return(final)

'''
This is where the GUI code starts
'''
import tkinter as tk
from tkinter import ttk
#font types
TITLE_FONT = ("Verdana", 14,) #"bold")
LARGE_FONT = ("Verdana", 12)
MEDIUM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)
class AllWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #add title
        tk.Tk.wm_title(self, "QIIME 2 Cleaner")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        #create navigation menu
        menubar = tk.Menu(container)
        navimenu = tk.Menu(menubar, tearoff=0)
        #add quit button in menu that triggers a command
        navimenu.add_command(label="Quit", command=self.die)
        #actually add the bar
        menubar.add_cascade(label="Menu", menu=navimenu)
        tk.Tk.config(self, menu=menubar)
        #show the frames
        self.frames = {}
        frame = HomePage(container, self)
        #set background color for the pages
        frame.config(bg='white')
        self.frames[HomePage] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(HomePage)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    #end program fcn triggered by quit button
    def die(self):
        exit()
#add home page
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="QIIME 2 Output Selector & Community Composition Plotter", bg='white', font = TITLE_FONT).grid(row=0, columnspan=14, pady = (15,0))
        #feature table entry
        feature_path = tk.StringVar()
        self.featuretable_label = tk.Label(self,bg = 'white', width = 35, anchor = 'e', text="Collapsed feature table path: ")
        self.featuretable_entry = tk.Entry(self, width = 80, textvariable = feature_path)
        self.featuretable_entry.insert(0, 'Ex. C:\Research/collapsed-feature-table.tsv')
        self.featuretable_label.grid(row=4, column = 1, padx = (0,10), pady = (30,0))
        self.featuretable_entry.grid(row=4, column = 2, padx = (0,50), pady = (30,0))
        #output csv path
        output_path = tk.StringVar()
        self.output_label = tk.Label(self,bg = 'white', width = 35, anchor = 'e', text="Output CSV path: ")
        self.output_entry = tk.Entry(self, width = 80, textvariable = output_path)
        self.output_entry.insert(0, 'Ex. C:\Research/output.csv')
        self.output_label.grid(row=5, column = 1, padx = (0,10), pady = (10,0))
        self.output_entry.grid(row=5, column = 2, padx = (0,50), pady = (10,0))
        #selection number
        selection_num = tk.StringVar()
        self.select_label = tk.Label(self,bg = 'white', width = 35, anchor = 'e', text="Number of top taxa to select per sample: ")
        self.select_entry = tk.Entry(self, width = 80, textvariable = selection_num)
        self.select_entry.insert(0, 'Enter integer here')
        self.select_label.grid(row=6, column = 1, padx = (0,10), pady = (10,0))
        self.select_entry.grid(row=6, column = 2, padx = (0,50), pady = (10,0))
        #graph name
        graph_name = tk.StringVar()
        self.graphname_label = tk.Label(self,bg = 'white', width = 35, anchor = 'e', text="Title of community composition graph: ")
        self.graphname_entry = tk.Entry(self, width = 80, textvariable = graph_name)
        self.graphname_entry.insert(0, 'Enter graph title here')
        self.graphname_label.grid(row=7, column = 1, padx = (0,10), pady = (10,0))
        self.graphname_entry.grid(row=7, column = 2, padx = (0,50), pady = (10,0))
        #graph legend size
        legend_size = tk.StringVar()
        self.legend_label = tk.Label(self,bg = 'white', width = 35, anchor = 'e', text="Enter graph legend font size: ")
        self.legend_entry = tk.Entry(self, width = 80, textvariable = legend_size)
        self.legend_entry.insert(0, 'Enter integer here (suggested is 8)')
        self.legend_label.grid(row=8, column = 1, padx = (0,10), pady = (10,0))
        self.legend_entry.grid(row=8, column = 2, padx = (0,50), pady = (10,0))
        #graph legend text padding
        legend_pad = tk.StringVar()
        self.legend_pad_label = tk.Label(self,bg = 'white', width = 35, anchor = 'e', text="Enter graph legend text padding: ")
        self.legend_pad_entry = tk.Entry(self, width = 80, textvariable = legend_pad)
        self.legend_pad_entry.insert(0, 'Enter integer here (suggested is 0.5)')
        self.legend_pad_label.grid(row=9, column = 1, padx = (0,10), pady = (10,0))
        self.legend_pad_entry.grid(row=9, column = 2, padx = (0,50), pady = (10,0))
        #button widget
        output_button = ttk.Button(self, text="Generate Output CSV & Plot Graph",
                            command=self.gen_output)
        output_button.grid(row=10, columnspan=14, pady= (15,0))
        #explanation
        self.explain1 = tk.Label(self,bg = 'white', width = 100, anchor = 'e', justify = 'left', text="*Input table must be the collapsed table TSV file from QIIME 2\n*Make sure to enter absolute file paths for all input tables\n*The inputs for taxonomic level, number of top taxa to select per sample, and graph legend font size must be integers\n*The example path given is in Windows format, Linux and macOS users will need to use a different path structure")
        self.explain11 = tk.Label(self,bg = 'white', width = 120, anchor = 'e', justify = 'left', text="*Avoid editing the TSV input files using Excel prior to entering it into this program to avoid empty lines being added and disrupting the sorting process")
        self.explain2 = tk.Label(self,bg = 'white', width = 110, anchor = 'e', justify = 'left', text="*This tool is ONLY optimized for the collapsed feature table outputs from qiime2-2020-2 using the Naive Bayes classifier trained on \n Silva 138 99% OTUs from the 515F/806R region of sequences, and using this with other classifiers or bioinformatics packages may require\n some adjustments")
        self.explain3 = tk.Label(self,bg = 'white', width = 20, anchor = 'e', justify = 'left', text='Credit: Bill Yen')
        self.explain1.place(x=25,y=400)
        self.explain11.place(x=62,y=463)
        self.explain2.place(x=60,y=490)
        self.explain3.place(x=46,y=620)
        #configure grid
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(5, weight=3)
    def gen_output(self):
        concatenated, header_row, sample_names, total = taxonomy_arranger(self.featuretable_entry.get())
        #the number in the input here represents where you truncate the data (10 means top 10 taxa in each samples, etc.)
        import numpy as np
        #np.savetxt("E:\Research/test_output.csv", concatenated, delimiter = ',', fmt='%s')
        final = topsearcher(concatenated, int(self.select_entry.get()), total, sample_names)
        #np.savetxt("E:\Research/test_output3.csv", final, delimiter = ',', fmt='%s')
        import matplotlib.pyplot as plt
        import matplotlib.colors as mcolors
        from matplotlib import style
        style.use("seaborn-muted")
        import numpy as np
        import pandas as pd
        pd.options.mode.chained_assignment = None  # default='warn'
        raw_data = pd.DataFrame(data=final,columns=header_row,dtype=float)
        #convert to percentage
        raw_data_percent = pd.DataFrame()
        percentage1 = raw_data.groupby(['#OTU ID'])
        percentage1 = percentage1[[sample_names[0]]].sum()
        percentage1 = percentage1.apply(lambda x: x/x.sum()).reset_index()
        raw_data_percent = percentage1['#OTU ID']
        for ii in range(len(sample_names)):
            percentage = raw_data.groupby(['#OTU ID'])
            percentage = percentage[[sample_names[ii]]].sum()
            percentage = percentage.apply(lambda x: x/x.sum()).reset_index()
            raw_data_percent = pd.concat([raw_data_percent, percentage[sample_names[ii]]], axis =1)
        #sort data in descending order, then transpose data for graphing
        raw_data_percent = raw_data_percent.sort_values(by=sample_names[0], ascending = False)
        header_row = raw_data_percent['#OTU ID'].tolist()
        raw_data_percent = raw_data_percent.transpose().drop(['#OTU ID'])
        raw_data_percent.columns = header_row
        #making a bigger colormap by combining smaller default ones
        colors1 = plt.cm.tab20b(np.linspace(0, 1, 20))
        colors2 = plt.cm.tab20c(np.linspace(0, 1, 20))
        colors3 = plt.cm.coolwarm(np.linspace(0, 1, 12))
        colors4 = plt.cm.Paired(np.linspace(0, 1, 12))
        colors5 = plt.cm.Pastel2(np.linspace(0, 1, 8))
        colors = np.vstack((colors1, colors2, colors3, colors5,colors4))
        mymap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)
        ax = raw_data_percent.plot(kind="barh", stacked=True, width = 0.8, colormap = mymap)
        plt.suptitle(self.graphname_entry.get(),fontsize=15)
        plt.ylabel("Sample Names")
        plt.xlabel("Relative Abundance")
        # configure y tick labels to match sample name
        ax.set_yticklabels(sample_names)
        #configure graph layouts
        plt.tight_layout()
        plt.subplots_adjust(right=0.8, top=0.9)
        #make legend and plot the graph
        plt.legend(loc='upper left', frameon = False, bbox_to_anchor=(1,1), handletextpad = float(self.legend_pad_entry.get()), fontsize = int(self.legend_entry.get()), labelspacing = 0.5, ncol=1)
        #fix output to export to csv
        final_data = raw_data
        for ii in range(len(final_data['#OTU ID'])):
            final_data['#OTU ID'][ii] = final_data['#OTU ID'][ii].replace('$\\it{','')
            final_data['#OTU ID'][ii] = final_data['#OTU ID'][ii].replace('}$','')
            final_data['#OTU ID'][ii] = final_data['#OTU ID'][ii].replace('\ ',' ')
        #get rid of number index for the rows
        final_data.to_csv(self.output_entry.get(), index = False)
        plt.show()
app = AllWindow()
app.geometry('1025x672')
#mainloop
app.mainloop()