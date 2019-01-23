# clean_outreg2

get xml files from outreg2 in Stata, then run 

python3 clean_outreg2 -i <input_files> -d <var dict> -o <output directory>

to get a tex file for you to include in latex documents

You can specify \tabular environment freely, because this just output all data rows. var dict should have a json file specifies how do you want to change the name of the variables to better names in latex.

the input files can be glob argument, for example, *.xml will point to all xml files in the directory and convert them all. Or, you can specify multiple files using comma, for example, a.xml,b.xml ...
