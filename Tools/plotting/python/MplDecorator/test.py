import MplDecorator
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import os


x = np.linspace(0, 3)
y = np.random.normal(x*2,2,len(x))
z = np.random.normal(-x*5,2,len(x))
df = pd.DataFrame({"Time":x,"y":y,"z":z})
df = df.melt("Time")



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
