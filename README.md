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
 
Data files:
All data files are in the subdirectory /data.
-dta_texts_18c.csv: A list of 18th century texts from the DTA corpus (Deutsches Textarchiv, www.deutschestextarchiv.de)
-isch_18c.csv: A list of occurences of -isch formations in the DTA from the 18th century
-nis_18c.csv: A list of occurences of -nis formations in the DTA from the 18th century
-texts_dta.csv: A list of texts from the DTA corpus
-isch.csv: A list of occurences of -isch formations in the DTA
-nis.csv: A list of occurences of -nis formations in the DTA
-tum.csv: A list of occurences of -tum formations in the DTA

1. säily_nis_CLLT.py, säily_isch_CLLT.py
The Monte Carlo simulations for the Säily plots are computed in two files, säily_nis_CLLT.py and säily_isch_CLLT.py. These files take as input a list of occurrences (isch_18c.csv, nis_18c.csv), and a list of all 18th century texts in the corpus (dta_texts_18c.csv). The output of the scripts is a) a list of files together with the set of distinct words (with -isch/-nis) in them and b) a table with one row per simulation and one row per decade that contains the values for the respective number of types divided by the number of running words (isch_types_over_tokens.csv, nis_types_over_tokens.csv).
The number of simulations is set to 100; in the paper, 100,000 simulations are used, but this takes about 1-2 days on a new MacBook.

2. plot_1_CLLT.py, plot_2_CLLT.py
These scripts plot figure 1 and 2 in the paper. They use the output of the last scripts (isch_types_over_tokens.csv, nis_types_over_tokens.csv) as input and save a png file to the /plots directory.

3. plot_3_CLLT.py
This script produces plot 3 in the paper: It compares the mean type value of all simulations with the actual observed value for the decades and saves a plot of the results. It also computes Spearman's rho for the correlations.

4. isch_monte_carlo_CLLT.py, nis_monte_carlo_CLLT.py, tum_monte_carlo_CLLT.py
These scripts compute the Monte Carlo simulations for the Pneo values (which are in turn the basis for figure 4 and 5). They take as input the list of files (texts_dta.csv) and the list of occurrences of the respective pattern (isch.csv, nis.csv, and tum.csv). The number of simulations is set to 100; in the paper, 100,000 simulations are used.

5. plot_4_CLLT.py, plot_5_CLLT.py
These scripts produce plot 4 in the paper, a Pneo plot for -isch and -nis, and plot 5, a Pneo plot for -tum. They use the output of the last scripts as input, and they save a png fie to the /plots directory.
