# CLLT
Python scripts for a Corpus Linguistics and Linguistic Theory paper ("Productivity, vocabulary size, and new words"). 

Requirements:
-Python 3.x
-Packages:
  -numpy
  -scipy
  -pylab
  -matplotlib
  -timeit
  -pandas
  -itertools
 
Data:

1. säily_nis_CLLT.py, säily_isch_CLLT.py
The Monte Carlo simulations for the Säily plots are computed in two files, säily_nis_CLLT.py and säily_isch_CLLT.py. These files take as input a list of occurrences (isch_18c.csv, nis_18c.csv), and a list of all texts in the corpus (dta_texts_18c.csv). The output of the scripts is a) a list of files together with the set of distinct words (with -isch/-nis) in them and b) a table with one row per simulation and one row per decade that contains the values for the respective number of types divided by the number of running words (isch_types_over_tokens.csv, nis_types_over_tokens.csv).
The number of simulations is set to 100; in the paper, 100,000 simulations are used, but this takes about 1-2 days on a new MacBook.

2. plot_1_CLLT.py, plot_2_CLLT.py
These scripts plot figure 1 and 2 in the paper. They use the output of the last scripts (isch_types_over_tokens.csv, nis_types_over_tokens.csv) as input and save a png file.

3. plot_3_CLLT.py
