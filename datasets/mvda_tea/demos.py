#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, March 2017

import pylab
import numpy as np
from datasets.mvda_tea import load_mvda_tea

# ---------------------------------------------------------------


def plot_mvda_tea_data_set():
    # loading the mvda tea data set
    ds = load_mvda_tea()

    # removing columns associated with classes and properties
    ds = ds.iloc[:, :-1]

    # plotting the data set
    ds.T.plot(legend=None)
    pylab.show()


def plot_mvda_tea_by_variety():
    # loading the mvda tea data set
    ds = load_mvda_tea()

    # getting unique set of varieties
    y = np.unique(ds['variety'].tolist())

    # creating the figure and adding subplots
    n_rows, n_cols = 2, 3
    fig, axes = pylab.subplots(nrows=n_rows, ncols=n_cols)

    # for each variety
    for idx, label in enumerate(y):
        i, j = int(idx / n_cols), idx % n_cols
        axes[i][j].set_title(label)
        ds[ds['variety'] == label].iloc[:, :-2].T.plot(ax=axes[i][j], legend=None)

    # actually showing the plot
    pylab.show()


def plot_mvda_tea_by_type():
    # loading the mvda tea data set
    ds = load_mvda_tea()

    # getting unique set of varieties
    y = np.unique(ds['type'].tolist())

    # creating the figure and adding subplots
    n_rows, n_cols = 1, 3
    fig, axes = pylab.subplots(nrows=n_rows, ncols=n_cols)

    # for each variety
    for idx, label in enumerate(y):
        axes[idx].set_title(label)
        ds[ds['type'] == label].iloc[:, :-2].T.plot(ax=axes[idx], legend=None)

    # actually showing the plot
    pylab.show()
