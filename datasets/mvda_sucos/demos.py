#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, March 2017

import pylab
import numpy as np
from datasets.mvda_sucos import load_mvda_sucos

# ---------------------------------------------------------------


def plot_mvda_sucos_data_set():
    # loading the mvda sucos data set
    ds = load_mvda_sucos()

    # removing columns associated with classes and properties
    ds = ds.iloc[:, :-1]

    # plotting the data set
    ds.T.plot(legend=None)
    pylab.show()


def plot_mvda_sucos_by_class():
    # loading the mvda sucos data set
    ds = load_mvda_sucos()

    y = np.unique(ds['class'].tolist())

    # creating the figure and adding subplots
    n_rows, n_cols = 2, 4
    fig, axes = pylab.subplots(nrows=2, ncols=4)

    for idx, label in enumerate(y):
        i, j = int(idx / n_cols), idx % n_cols
        axes[i][j].set_title(label)
        ds[ds['class'] == label].iloc[:, :-1].T.plot(ax=axes[i][j], legend=None)

    # actually showing the plot
    pylab.show()
