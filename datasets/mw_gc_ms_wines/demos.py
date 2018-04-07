#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, February 2017

import numpy as np
import pylab
from matplotlib import cm
from mpl_toolkits.mplot3d import axes3d

from datasets.mw_gc_ms_wines import load_mw_gc_ms_wines

# ---------------------------------------------------------------


def plot_mw_gc_ms_wines_data_set():
    # loading the 'mw_gc_ms_wines' data set
    ds = load_mw_gc_ms_wines()

    # gettting GC-MS aligned data
    gc_ms_aligned = ds['gc_ms_aligned']

    elution_range = np.array(gc_ms_aligned.major_axis.tolist())
    profiles_range = np.array(gc_ms_aligned.minor_axis.tolist())

    # computing the grid for all samples
    X, Y = np.meshgrid(elution_range, profiles_range)
    X, Y = X.T, Y.T # transposing X and Y, as meshgrid changes the order of axis

    Z = gc_ms_aligned.iloc[0, :, :].values

    fig = pylab.figure()
    ax = fig.gca(projection='3d')

    ax.set_title('Wine sample: {}'.format(gc_ms_aligned.items[0]))
    ax.plot_surface(X, Y, Z, rstride=8, cstride=8, cmap=cm.coolwarm, linewidth=0, antialiased=False)

    # actually showing the plot
    pylab.show()
