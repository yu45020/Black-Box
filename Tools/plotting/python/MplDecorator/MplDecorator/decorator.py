# -*- coding: utf-8 -*-

from functools import wraps
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

__all__ = ['MplDecorator', ]


class MplDecorator:
    """
    Decorator for plotting functions.
    It updates matplotlib's rcParams only for the decorated functions
    """

    def __init__(self, mpl_rcp, sns_style=None):
        self.mpl_rcParams = mpl_rcp
        self.sns_style = sns_style

    def __call__(self, func, *args, **kwargs):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with plt.rc_context(self.mpl_rcParams):
                plt.style.use(self.sns_style)
                plt.rcParams.update(self.mpl_rcParams)

                return func(*args, **kwargs)

        return wrapper
