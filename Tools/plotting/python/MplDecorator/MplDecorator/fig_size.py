# -*- coding: utf-8 -*-

def fig_size(fig_width_in = 4.85678, fig_height_in=None):
    """
    :param fig_width_in:
    :param fig_height_in:
    :return: default tuple (4.85678, 3.00165)
    """
    GOLDEN_RATIO = 0.6180339887498949
    if fig_height_in is None:
        ratio = GOLDEN_RATIO
    else:
        ratio = fig_width_in/fig_height_in

    fig_height_in = fig_width_in*ratio

    return (fig_width_in, fig_height_in)