# MplDecorator

Python decorator for matplotlib and seaborn plots. Users only need to add one line on top of a plotting function to set pre-customized styles without changing current plot styles. The current version support LaTex decorator.

This tool is built on
[Yi-Xin Liu's mpltex](https://github.com/liuyxpp/mpltex) and 
[masasin's latexipy](https://github.com/masasin/latexipy)

R users may want to check ggpubr to easily get publication-ready plots.


## Installing

1. Download the package and unzip it.
2. In terminal and the directory of the package, run 
    ```
    python setup.py install
    ```

## Known Issues
1. Must define a plot function to use the decorator.
2. In order to save in eps format, plots must be saved inside the plot function. Saving in PDF format will result in error (may be use.LaTex error)
3. To convert a eps file to PDF, insert them into a latex file and compile that file, or type the following code in terminal
    ```
    epstopdf "file_name.eps"
    ```


## Available Decorators

### @MplDecorator.latex_decorator
```
Parameters can be customized in "latex.py": 

font size for all: 8
font family: serif
usetex: True
figure size: (width=4.296, height=2.655)
savefig format: eps
savefig.dpi: 900 
seaborn.style: 'seaborn-whitegrid' & "seaborn-paper"
```

## Prerequisites
Python 3

Python 2 is not tested yet.


## Sample Usages

``` python 
import os, sys
sys.path.append(os.getcwd())
import MplDecorator
import matplotlib.pyplot as plt
import numpy as np



x = np.linspace(0, 3)
y = np.sin(x)
z = np.cos(x)

@MplDecorator.latex_decorator
def text_plot():
    fig,ax = plt.subplots()
    # fig, ax = plt.subplots(figsize=(11,11))
    line_style = MplDecorator.linestyles()
    next(line_style)
    ax.plot(x,y,label='y', **next(line_style))
    ax.plot(x,z, label='z', **next(line_style))
    ax.set_title("With Decorator")
    ax.set_xlabel('Some x')
    ax.set_ylabel('Some y')
    ax.legend(loc='best')
    fig.savefig("With Decorator.eps")

text_plot()
os.system('epstopdf "With Decorator.eps"')
```

![with decorator](https://user-images.githubusercontent.com/28139045/33397655-29ba6880-d501-11e7-9068-ad3b96f1981d.png)

```python
def text_plot2():
    #sns.lmplot(x="Time", y="value", hue="variable", data=dat)
    fig,ax = plt.subplots()
    line_style = MplDecorator.linestyles()
    next(line_style)
    ax.plot(x,y,label='y', **next(line_style))
    ax.plot(x,z, label='z', **next(line_style))
    ax.set_title("No Decorator")
    ax.set_xlabel('Some x')
    ax.set_ylabel('Some y')
    ax.legend(loc='best')
    fig.savefig("After Decorator.eps")

text_plot2()
os.system('epstopdf "After Decorator.eps"')
```
![no decorator](https://user-images.githubusercontent.com/28139045/33397652-29557146-d501-11e7-9967-7fefa71fd639.png)

```python
@MplDecorator.latex_decorator
def text_plot_larger():
    fig,ax = plt.subplots(figsize=(6,6))
    # fig, ax = plt.subplots(figsize=(11,11))
    line_style = MplDecorator.linestyles()
    next(line_style)
    ax.plot(x,y,label='y', **next(line_style))
    ax.plot(x,z, label='z', **next(line_style))
    ax.set_title("Larger With Decorator")
    ax.set_xlabel('Some x')
    ax.set_ylabel('Some y')
    ax.legend(loc='best')
    fig.savefig("With Decorator Larger.eps")

text_plot_larger()
os.system('epstopdf "With Decorator Larger.eps"')
```
![with decorator larger](https://user-images.githubusercontent.com/28139045/33397653-299bd9f6-d501-11e7-8151-af068484866f.png)
