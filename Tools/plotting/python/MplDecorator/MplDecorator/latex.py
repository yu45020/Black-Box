# -*- coding: utf-8 -*-

from .decorator import *
from .fig_size import *
from .colors import *
from .fig_size import *

__all__ = ['latex_decorator', ]

FONT_SIZE = 8
mpl_params = {
    'font.family': 'sans-serif',
    'font.serif': ['Times', 'Computer Modern Roman'],
    'font.sans-serif': ['Helvetica', 'Arial', 'Computer Modern Sans serif'],
    'text.latex.unicode': True,
    'text.usetex': True,
    'text.latex.preamble': [r'\usepackage{siunitx}',
                            r'\sisetup{detect-all}',
                            r'\usepackage{helvet}',
                            r'\usepackage[eulergreek,EULERGREEK]{sansmath}',
                            r'\sansmath'],
    'axes.prop_cycle': default_color_cycler,

    'font.size': FONT_SIZE,
    'axes.labelsize': FONT_SIZE,
    'axes.titlesize': FONT_SIZE,
    'legend.fontsize': FONT_SIZE,
    'xtick.labelsize': FONT_SIZE,
    'ytick.labelsize': FONT_SIZE,

    'figure.figsize': fig_size(),  # default (4.85678, 3.00165)
    'figure.dpi': 600,
    'savefig.format': 'eps'
    # 'savefig.bbox': 'tight',
    # this will crop white spaces around images that will make
    # width/height no longer the same as the specified one.
}

sns_style = ['seaborn-whitegrid',"seaborn-paper"]

latex_decorator = MplDecorator(mpl_params, sns_style)
