# Qiime2-Output-Cleaner
This program takes the collapsed feature table TSV output from [QIIME 2](https://qiime2.org/), selects the top *n* most abundant taxa per sample (the user inputs how many taxa they want), and plots a community composition graph displaying those taxa in each sample. Unlike the built-in QIIME 2 taxonomy bar plot visualization, this allows the user to easily limit the community composition plot to only the most abundant taxa, which is important for visualizing samples with thousands of taxa present. This program was built on **Python 3.8.5** with **Matplotlib 3.2.2**, **pandas 1.0.5**, and **NumPy 1.19.0**, so adjustments might be needed if Qiime2-Output-Cleaner is used with past or future versions of Python and its associated libraries.

*Note: the existing code might not catch all of the unclear labels QIIME 2 throws in for the features' taxonomic labels ("AKYH767", "env.OPS 17", "UTCFX1", etc.). In the case that you end up with an unwanted label in the legend, you should go to the output CSV file, edit the name of the feature to your desired name based on what's in the original collapsed table, and plot it with your preferred graphing software (Excel, Python, R). Another option is to add that label to topsearcher() following the format for the replacement of "uncultivated" and go from there.*

## How To Use Qiime2-Output-Cleaner:
1. First, process your raw FASTA files with QIIME 2 and output the [collapsed feature table TSV file](https://docs.qiime2.org/2020.8/plugins/available/taxa/collapse/). Also make sure that the Python libraries mentioned above are all installed on your machine.
2. Run Qiime2-output-cleaner.py and follow the prompts in the labels and entry boxes to tell it where your input TSV file is, indicate where you want your output table saved to, customize the number of taxa you choose, and change the graph parameters. Note that the paths of the input and output files must include the actual name of the file itself, since those are not implied (e.g. "C:\Research/" won't work for an output path, you have to state "C:\Research/output.csv" to make a CSV called output.csv there). **The output file must end with ".csv".**
3. After making sure that all your entries are right, press "Generate Output CSV & Plot Graph" to create your output CSV and graph. The time it takes to run will depend on the size of your dataset and the number of top taxa you selected for. If your entries are invalid, an error message will show up in the terminal you used to run Qiime2-output-cleaner.py. **Caution: the number of unique colors for the legend patches is around 70, so choosing too many taxa to display will result in duplicate colors.**
4. A popup window displaying the desired graph should appear within a few seconds, and the output file will be saved to your specified path at the same time. You can then use the Matplotlib toolbar on the bottom of the graph window to zoom in on parts of the graph or manipulate its width and height. When you are satisfied with the graph format, press the "Save" button on the toolbar to save your graph as a PNG. The program can be used continuously, so you can experiment with the legend font size and title text in the main window or enter in new datasets without having to rerun the Python file.
5. Congratulations! You now have a sorted CSV file displaying the top *n* taxa in your samples and a community composition graph to visualize it.
