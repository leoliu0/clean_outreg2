import getopt
import json
import os
import sys
import xml.etree.ElementTree as ET
from glob import glob

def proc_file(f):
    tree = ET.parse(f)
    root = tree.getroot()
    global hline_count
    hline_count = False
    with open(os.path.join(output_dir,f.replace('.xml','.tex')),'w',newline='') as wf:
        wf.write('\hline\\\\ \n')
        for x in root:
            if x.attrib:
                for y in x:
                    for k,v in y.attrib.items():
                        if 'ExpandedColumnCount' in k:
                            global cols
                            cols = int(v)                
                    for z in y:
                        if 'Row' in z.tag:
                            if list(z) and len(list(z))==cols:
                                newrow = proc_row(z.findall('.//{urn:schemas-microsoft-com:office:spreadsheet}Data'))
                                if newrow:
                                    wf.write(newrow + ' \n')
        wf.write('\hline\\\\ \n')


def proc_row(row):
    row = [e.text for e in row]
    none_count = 0
    dot_count = 0
    cells = []
    for cell in row:
        if cell == 'VARIABLES':
            cell = ''
        if cell is None:
            none_count += 1
            cell = ''
        else:
            if (cell == '(.)') or (cell == '.'):
                dot_count += 1
                cell = ''
            if vardict:
                if cell in vardict:
                    cell = vardict[cell]
        cells.append(cell)
    if cols == none_count:
        global hline_count
        if hline_count is False:
            hline_count = True
            return '\hline\\\\'+ '& '*(cols-1) + '\\\\'.strip('"')
        else:
            return '& '*(cols-1) + '\\\\'
    if cols - (none_count + dot_count) <= 1:
        return
    return '& '.join(cells) + '\\\\'    

def main(argv):
    global vardict     
    global output_dir
    inputfiles,vardict,output_dir = '','',''    
    try:
        opts, args = getopt.getopt(argv,"hi:d:o:")
    except getopt.GetoptError:
        print ('clean_outreg2.py -i <inputfile(s)> -d(optional) <var dict> -o(optional) <output directory>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('clean_outreg2.py -i <inputfile(s)> -d(optional) <var dict> -o(optional) <output directory>')
        elif opt == '-i':
            inputfiles = arg
        elif opt == '-d':
            vardict = arg
        elif opt == '-o':
            output_dir = arg
    if ',' in inputfiles:
        files = inputfiles.split(',')
    else:
        files = glob(inputfiles)
    
    if vardict:
        with open(vardict,'r') as f:
            vardict = json.load(f)

    for f in files:
        proc_file(f)

if __name__ == "__main__":
   main(sys.argv[1:])
