# Qiime2-Output-Cleaner
This program takes the feature-table and taxonomy CSV output from Qiime2, selects the top n most abundant taxa per sample, and plots a community composition graph displaying those taxa in each sample. Unlike the built-in Qiime2 taxonomy bar plot visualization, this allows the user to easily limit the community composition plot to the most abundant taxa, which is important for visualizating samples with thousands of taxa present. This program was built on Python 3.8.5 and requires the use of Matplotlib 3.2.2, Pandas 1.0.5, and Numpy 1.19.0.
