"""
Need file name as input argument.

Run the following:
    1. pdflatex filename.tex
    2. check whether bcf file exists ==> the file use biber
    3. del aux files except .synctex.gz, which enables view and go to source in TexStduio

How to use:
    a. Suppose in TexStudio, option --> build --> user commands, create a command and type:
        python "path to latex_clear_aux.py" %
        (need double quote outside of the path)
    b. copy the following to meta command: "build & view"
        txs:///"new command name" | txs:///view
        (Note: the new command name can be selected in config draw down)

"""

import os
import glob
import subprocess
import argparse
from sys import platform


def del_aux(file_name):
    file = glob.glob(file_name + ".*", recursive=False)

    file = list(filter(not_pdf_tex_gz, file))
    file = list(filter(not_folder, file))

    System = platform
    if file:
        if System == 'win32':
            [os.remove(x) for x in file]
            subprocess.run(['attrib', "+h", file_name + ".synctex.gz"], timeout=2)  # enable go to source in view pdf
        else:  # assume linux system
            [subprocess.run(['rm', x]) for x in file]
            if os.isfile(file_name + ".synctex.gz"):
                os.rename(file_name + ".synctex.gz", "." + file_name + ".synctex.gz")


def not_folder(file_name):
    return not os.path.isdir(file_name)

def not_pdf_tex_gz(file_name):
    return not (file_name.endswith('.pdf') or file_name.endswith('.tex') or file_name.endswith('.gz'))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", type=str)
    file_name = parser.parse_args().file_name

    pdflatex_args = "-synctex=1 -interaction=nonstopmode"
    subprocess.run(["pdflatex.exe", pdflatex_args, file_name + '.tex'], timeout=2)

    if os.path.isfile(file_name + ".bcf"):
        subprocess.run(["biber.exe", file_name + ".bcf"], timeout=2)
        subprocess.run(["pdflatex.exe", pdflatex_args, file_name + '.tex'], timeout=2)

    del_aux(file_name)

