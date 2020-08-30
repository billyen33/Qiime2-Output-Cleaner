'''
taxonomy_selector replaces D_0__, D_1__, etc with d, p, c, etc.
It also reduces the taxonomy assignment for each feature ID to its most specific level up till the genus level
'''
#remember to split by semicolon too
def taxonomy_selector(input_file, taxa_level):
    import re
    Taxon_assignment = []
    with open(input_file,'r') as file:
        f = file.read().split('\n')
        for line in f:
            line = line.replace(',,', ',')
            line = re.split(';|,',line)
            line = [i for i in line if i]
            length = len(line)
            if length >= taxa_level:
                index = taxa_level - 1
                if "Subgroup" not in line[index]:
                    if "uncultured" not in line[index] and "uncultivated" not in line[index]:
                        if "D_5__" in line[index] or "g " in line[index]:
                            ita_output = line[index].replace("D_5__", "g ")
                            ita_output = ita_output.split('g ')
                            ita_output[1] = "$\it{"+ita_output[1]+"}$"
                            real_output = "g " + ita_output[1]
                            Taxon_assignment.append(real_output)
                        elif "D_6__" in line[index] or "s " in line[index]:
                            ita_output = line[index].replace("D_6__", "s ")
                            ita_output = ita_output.split('s ')
                            ita_output[1] = "$\it{"+ita_output[1]+"}$"
                            real_output = "s " + ita_output[1]
                            Taxon_assignment.append(real_output)
                        else:
                            Taxon_assignment.append(line[index])
                    else: #this means it contains "uncultured" or "uncultivated"
                        for ii in range(index+1):
                            if "uncultured" not in line[index-ii] and "uncultivated" not in line[index-ii] and "Subgroup" not in line[index-ii]:
                                Taxon_assignment.append(line[index-ii])
                                break #exits for loop and move on to next line on csv   
                            elif "Subgroup" in line[index-ii]:    
                                for jj in range(index+1):
                                    if "Subgroup" not in line[index-jj] and "uncultured" not in line[index-jj] and "uncultivated" not in line[index-jj]:
                                        Taxon_assignment.append(line[index-jj] + " (" + line[index-ii] + ")")
                                        break
                                    #else this moves on to next item on the list and checks again
                                break
                            # if none of those triggers, then "uncultured"/"uncultivated" is in there again
                else: #this means "Subgroup" is in the cell
                    for ii in range(index+1):
                        if "Subgroup" not in line[index-ii] and "uncultured" not in line[index-ii] and "uncultivated" not in line[index-ii]:
                            if "D_5__" in line[index] or "g " in line[index]:
                                ita_output = line[index].replace("D_5__", "g ")
                                ita_output = ita_output.split('g ')
                                ita_output[1] = "$\it{"+ita_output[1]+"}$"
                                real_output = "g " + ita_output[1]
                                Taxon_assignment.append(line[index-ii] + " (" + real_output + ")")
                                break
                            elif "D_6__" in line[index] or "s " in line[index]:
                                ita_output = line[index].replace("D_6__", "s ")
                                ita_output = ita_output.split('s ')
                                ita_output[1] = "$\it{"+ita_output[1]+"}$"
                                real_output = "s " + ita_output[1]
                                Taxon_assignment.append(real_output)
                                break
                            else:
                                Taxon_assignment.append(line[index-ii] + " (" + line[index-ii] + ")")
                                break
            else: #this means the line doesn't have enough items, so we use the length of line instead
                length = length-1
                if "Subgroup" not in line[length]:
                    if "uncultured" not in line[length] and "uncultivated" not in line[length]:
                        if "D_5__" in line[length] or "g " in line[length]:
                            ita_output = line[length].replace("D_5__", "g ")
                            ita_output = ita_output.split('g ')
                            ita_output[1] = "$\it{"+ita_output[1]+"}$"
                            real_output = "g " + ita_output[1]
                            Taxon_assignment.append(real_output)
                        elif "D_6__" in line[length] or "s " in line[length]:
                            ita_output = line[length].replace("D_6__", "s ")
                            ita_output = ita_output.split('s ')
                            ita_output[1] = "$\it{"+ita_output[1]+"}$"
                            real_output = "s " + ita_output[1]
                            Taxon_assignment.append(real_output)
                        else:
                            Taxon_assignment.append(line[length])
                    else: #this means it contains "uncultured" or "uncultivated"
                        for ii in range(length+1):
                            if "uncultured" not in line[length-ii] and "uncultivated" not in line[length-ii] and "Subgroup" not in line[length-ii]:
                                Taxon_assignment.append(line[length-ii])
                                break #exits for loop and move on to next line on csv   
                            elif "Subgroup" in line[length-ii]:    
                                for jj in range(length+1):
                                    if "Subgroup" not in line[length-jj] and "uncultured" not in line[length-jj] and "uncultivated" not in line[length-jj]:
                                        Taxon_assignment.append(line[length-jj] + " (" + line[length-ii] + ")")
                                        break
                                    #else this moves on to next item on the list and checks again
                                break
                            # if none of those triggers, then "uncultured"/"uncultivated" is in there again
                else: #this means "Subgroup" is in the cell
                    for ii in range(length+1):
                        if "Subgroup" not in line[length-ii] and "uncultured" not in line[length-ii] and "uncultivated" not in line[length-ii]:
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
    return output
'''
taxonomy_combiner combines rows with the same taxa values and arrange them from greatest to smallest to prepare for truncating in top10searcher
'''
def taxonomy_combiner(input_file, Taxon_assignment):
    #this part inserts the appropriate taxonomy assignment
    new_f = []
    with open(input_file,'r') as file:
            f = file.read().split('\n')
            for ii in range(1,len(f)):
                f[ii] = f[ii].split(',')
                f[ii][0] = Taxon_assignment[ii-1]    
            replaced_output = f[1:len(f)]
            key = replaced_output[0][1:]
            header_row = replaced_output[0]
            sample_names = header_row[1:]
    import pandas as pd
    import numpy as np
    df = pd.DataFrame(replaced_output[1:])
    df_taxa = df[0]
    df = df.drop([0],axis=1) #get the columns with no taxa column
    df = df.astype(int) #turn all the numbers to integers
    #generate sum of counts for all samples as a list
    total = []
    for ii in range(1,len(key)+1):
        total.append(df[ii].sum())
    df.insert(loc=0,column=0,value=df_taxa) #put the taxa column back
    df.columns= header_row #change the names of the columns to header_row
    df = df.groupby(['Taxon'], as_index = False).sum()
    #insert more taxa column so we can sort
    df_taxa = df['Taxon']
    for ii in range(1,len(df.columns)-1):
        #print(ii)
        label = 'Taxon' + str(2*ii)
        df.insert(loc=2*ii,column=label,value=df_taxa)
    #get rid of the index column
    df.set_index('Taxon',inplace=False)
    #now we sort by abundance
    #print(df.iloc[:,[0,1]])
    #split_frames = [df.iloc[:,[0,0+1]], df.iloc[:,[2,2+1]]]
    split_frames = []
    new_header = df.columns
    for ii in range(8):
        split_frames.append(df.iloc[:,[ii*2,(2*ii)+1]].sort_values(by=new_header[(ii*2)+1], ascending=False))
    concatenated = split_frames[0].to_numpy()
    #print(split_frames)
    for ii in range(1,len(split_frames)): #now we merge them back to df with numpy array
        split_frames[ii] = split_frames[ii].to_numpy()
        concatenated = np.concatenate((concatenated,split_frames[ii]), axis = 1)
        #split_frames[0].merge(split_frames[ii], left_on=new_header[0], right_on=new_header[ii*2])
        #new_df = split_frames[0]        
        #concatenated = pd.concat([concatenated,split_frames[ii]], axis=1)
    header = df.columns.to_numpy()
    concatenated = np.vstack((header,concatenated))
    #save as csv
    #np.savetxt(file_path + "foo.csv", concatenated, fmt='%s', delimiter=",")
    return(concatenated, header_row, sample_names, total)
'''
topsearcher seach for the top n number of taxa and truncate the data to that, the rest of the sequence values is combined to an "Others" row
input_array is the output from taxonomy_selector, output_file is where the output is saved to, header_row and total are things that are needed for plotting
top_taxa is how you specify how many top taxa to take from each sample (Warning: too many will result in gigantic legend unless you decrease font size)
'''
def topsearcher(input_array, output_file, header_row, top_taxa, total, sample_names):
    import numpy as np
    import csv
    all_sample = [[],[],[],[],[],[],[],[]]
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
    #Generate "Others" row here
    init_array = np.array(final, dtype=object)
    num_array = np.delete(init_array,0,1).astype(float).astype(int)
    top_sum = num_array.sum(axis=0)
    others_array = total - top_sum
    others_array = others_array.astype(str)
    others_array = np.insert(others_array, 0, 'Others', axis=0)
    others_row = others_array.tolist()
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header_row)
        for i in range(taxa_num):
            writer.writerow(final[i])
        writer.writerow(others_row)

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
        tk.Tk.wm_title(self, "Qiime2 Cleaner")
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
        label = tk.Label(self, text="Qiime2 Output Selector & Community Composition Plotter", bg='white', font = TITLE_FONT).grid(row=0, columnspan=14, pady = (15,0))
        #feature table entry
        feature_path = tk.StringVar()
        self.featuretable_label = tk.Label(self,bg = 'white', width = 25, anchor = 'e', text="Feature table path: ")
        self.featuretable_entry = tk.Entry(self, width = 80, textvariable = feature_path)
        self.featuretable_entry.insert(0, 'Ex. E:\Research/Taxonomic Analysis - feature-table (raw).csv')
        self.featuretable_label.grid(row=4, column = 1, padx = (0,10), pady = (30,0))
        self.featuretable_entry.grid(row=4, column = 2, padx = (0,50), pady = (30,0))
        #taxonomy table entry
        taxa_path = tk.StringVar()
        self.taxatable_label = tk.Label(self,bg = 'white', width = 25, anchor = 'e', text="Taxonomy table path: ")
        self.taxatable_entry = tk.Entry(self, width = 80, textvariable = taxa_path)
        self.taxatable_entry.insert(0, 'Ex. E:\Research/Taxonomic Analysis - taxonomy.csv')
        self.taxatable_label.grid(row=5, column = 1, padx = (0,10), pady = (10,0))
        self.taxatable_entry.grid(row=5, column = 2, padx = (0,50), pady = (10,0))
        #output csv path
        output_path = tk.StringVar()
        self.output_label = tk.Label(self,bg = 'white', width = 25, anchor = 'e', text="Output CSV path: ")
        self.output_entry = tk.Entry(self, width = 80, textvariable = output_path)
        self.output_entry.insert(0, 'Ex. E:\Research/output.csv')
        self.output_label.grid(row=6, column = 1, padx = (0,10), pady = (10,0))
        self.output_entry.grid(row=6, column = 2, padx = (0,50), pady = (10,0))
        #selection number
        selection_num = tk.StringVar()
        self.select_label = tk.Label(self,bg = 'white', width = 35, anchor = 'e', text="Number of top taxa to select per sample: ")
        self.select_entry = tk.Entry(self, width = 80, textvariable = selection_num)
        self.select_entry.insert(0, 'Enter integer here')
        self.select_label.grid(row=7, column = 1, padx = (0,10), pady = (10,0))
        self.select_entry.grid(row=7, column = 2, padx = (0,50), pady = (10,0))
        #taxonomic level
        taxa_level = tk.StringVar()
        self.taxalevel_label = tk.Label(self,bg = 'white', width = 35, anchor = 'e', text="Taxonomic level to select to: ")
        self.taxalevel_entry = tk.Entry(self, width = 80, textvariable = taxa_level)
        self.taxalevel_entry.insert(0, 'For Domain enter 1, Kingdom 2, Phylum 3, Class 4, Order 5, Family 6, Genus 7, Species 8')
        self.taxalevel_label.grid(row=8, column = 1, padx = (0,10), pady = (10,0))
        self.taxalevel_entry.grid(row=8, column = 2, padx = (0,50), pady = (10,0))
        #graph name
        graph_name = tk.StringVar()
        self.graphname_label = tk.Label(self,bg = 'white', width = 35, anchor = 'e', text="Title of community composition graph: ")
        self.graphname_entry = tk.Entry(self, width = 80, textvariable = graph_name)
        self.graphname_entry.insert(0, 'Enter graph title here')
        self.graphname_label.grid(row=9, column = 1, padx = (0,10), pady = (10,0))
        self.graphname_entry.grid(row=9, column = 2, padx = (0,50), pady = (10,0))
        #graph legend size
        legend_size = tk.StringVar()
        self.legend_label = tk.Label(self,bg = 'white', width = 35, anchor = 'e', text="Enter graph legend font size: ")
        self.legend_entry = tk.Entry(self, width = 80, textvariable = legend_size)
        self.legend_entry.insert(0, 'Enter integer here (suggested is 8)')
        self.legend_label.grid(row=10, column = 1, padx = (0,10), pady = (10,0))
        self.legend_entry.grid(row=10, column = 2, padx = (0,50), pady = (10,0))
        #button widget
        output_button = ttk.Button(self, text="Generate Output CSV & Plot Graph",
                            command=self.gen_output)
        output_button.grid(row=11, columnspan=14, pady= (15,0))
        #explanation
        self.explain1 = tk.Label(self,bg = 'white', width = 100, anchor = 'e', justify = 'left', text="*Make sure to enter full path for all input tables\n*The inputs for taxonomic level, number of top taxa to select per sample, and graph legend font size must be integers\n*The example path given is in Windows format, Linux and macOS users will need to use a different path structure")
        self.explain2 = tk.Label(self,bg = 'white', width = 110, anchor = 'e', justify = 'left', text="*This tool is ONLY optimized for the taxonomic/feature table outputs from Qiime2-2020-2 using the Naive Bayes classifier trained on \n Silva 138 99% OTUs from the 515F/806R region of sequences, and using this with other classifier or bioinformatics package will not guarantee\n full functionality")
        self.explain3 = tk.Label(self,bg = 'white', width = 20, anchor = 'e', justify = 'left', text='Credit: Bill Yen')
        self.explain1.place(x=25,y=400)
        self.explain2.place(x=81,y=455)
        self.explain3.place(x=46,y=600)
        #configure grid
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(5, weight=3)
    def gen_output(self):
        #print(self.featuretable_entry.get())
        #genus is the 7th item on the list for taxonomy_selector
        concatenated, header_row, sample_names, total = taxonomy_combiner(self.featuretable_entry.get(), taxonomy_selector(self.taxatable_entry.get(), int(self.taxalevel_entry.get())))
        #the number in the input here represents where you truncate the data (10 means top 10 taxa in each samples, etc.)
        topsearcher(concatenated, self.output_entry.get(), header_row, int(self.select_entry.get()), total, sample_names)
        #Here are all the plotting stuff
        import matplotlib.pyplot as plt
        import matplotlib.colors as mcolors
        from matplotlib import style
        style.use("seaborn-muted")
        import numpy as np
        import pandas as pd
        raw_data = pd.read_csv(self.output_entry.get())
        #convert to percentage
        raw_data_percent = pd.DataFrame()
        percentage1 = raw_data.groupby(['Taxon'])
        percentage1 = percentage1[[sample_names[0]]].sum()
        percentage1 = percentage1.apply(lambda x: x/x.sum()).reset_index()
        raw_data_percent = percentage1['Taxon']
        for ii in range(len(sample_names)):
            percentage = raw_data.groupby(['Taxon'])
            percentage = percentage[[sample_names[ii]]].sum()
            percentage = percentage.apply(lambda x: x/x.sum()).reset_index()
            raw_data_percent = pd.concat([raw_data_percent, percentage[sample_names[ii]]], axis =1)
        #sort data in descending order, then transpose data for graphing
        raw_data_percent = raw_data_percent.sort_values(by=sample_names[0], ascending = False)
        header_row = raw_data_percent['Taxon'].tolist()
        raw_data_percent = raw_data_percent.transpose().drop(['Taxon'])
        data_array = raw_data_percent.to_numpy()
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
        current_handles, current_labels = plt.gca().get_legend_handles_labels()
        plt.legend(loc='upper left', frameon = False, bbox_to_anchor=(1,1), handletextpad = 0.8, fontsize = int(self.legend_entry.get()), labelspacing = 0, ncol=1)
        plt.show()
        
app = AllWindow()
app.geometry('1025x672')
#mainloop
app.mainloop()




