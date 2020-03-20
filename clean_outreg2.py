import getopt
import json
import os
import sys
import xml.etree.ElementTree as ET
from glob import glob

print(
    'USAGE: python clean_outreg2.py -i <inputfile(s)> -d(optional) <var dict> -o(optional) <output directory>'
)


def proc_file(f):
    print('-----processing ', f)
    if '.xml' not in f:
        print('----------this is not xml file, skipped')
        return
    tree = ET.parse(f)
    root = tree.getroot()
    global hline_count
    hline_count = False
    output_file = os.path.join(
        output_dir.replace('"', '').replace("'", ''),
        os.path.split(f)[-1].replace('.xml', '.tex'))

    with open(output_file, 'w', newline='') as wf:
        print(output_file, ' Saved')
        for x in root:
            if x.attrib:
                for y in x:
                    for k, v in y.attrib.items():
                        if 'ExpandedColumnCount' in k:
                            global cols
                            cols = int(v)
                    wf.write('& ' * (cols - 1) + '\\\\ \\hline')
                    for z in y:
                        if 'Row' in z.tag:
                            if list(z) and len(list(z)) == cols:
                                newrow = proc_row(
                                    z.findall(
                                        './/{urn:schemas-microsoft-com:office:spreadsheet}Data'
                                    ))
                                if newrow:
                                    wf.write(newrow + ' \n')
        wf.write('\hline\\\\ \n')


def proc_row(row):
    row = [e.text for e in row]
    none_count = 0
    dot_count = 0
    cells = []
    for n, cell in enumerate(row):
        # if n == 0:
        # none_count += 1
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
                if cell.strip() in vardict:
                    cell = vardict[cell.strip()]
        cell = cell.replace('#', '$\\times$').replace('_', ' ')
        cells.append(cell)
    if set(cells[1:]) == {''} and cells[0] != '':
        return '\\\\'
    if cols == none_count:
        global hline_count
        if hline_count is False:
            hline_count = True
            return '\hline\\\\' + '& ' * (cols - 1) + '\\\\'.strip('"')
        else:
            return '& ' * (cols - 1) + '\\\\'
    if cols - (none_count + dot_count) == 0:
        return
    return '& '.join(cells) + '\\\\'


def main(argv):
    global vardict
    global output_dir
    inputfiles, vardict, output_dir = '', '', ''
    try:
        opts, args = getopt.getopt(argv, "hi:d:o:")
        print(opts)
    except getopt.GetoptError:
        print(
            'clean_outreg2.py -i <inputfile(s)> -d(optional) <var dict> -o(optional) <output directory>'
        )
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(
                'clean_outreg2.py -i <inputfile(s)> -d(optional) <var dict> -o(optional) <output directory>'
            )
        elif opt == '-i':
            print(type(arg))
            print('------' + arg)
            inputfiles = arg
        elif opt == '-d':
            vardict = arg
        elif opt == '-o':
            output_dir = arg
    if ',' in inputfiles:
        files = [f.strip() for f in inputfiles.split(',')]
    else:
        files = glob(inputfiles)

    if vardict:
        with open(vardict, 'r') as f:
            vardict = json.load(f)
    print(f'processing {len(files)} files')
    for f in files:
        proc_file(f)


if __name__ == "__main__":
    main(sys.argv[1:])
