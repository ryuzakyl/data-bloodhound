#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, March 2017

import pylab
import numpy as np
from datasets.mvda_archeology import load_mvda_archeology

# ---------------------------------------------------------------


def plot_mvda_archeology_data_set():
    # loading the mvda archeology data set
    ds = load_mvda_archeology()

    # creating the figure and adding subplots
    n_rows, n_cols = 1, 2
    fig, axes = pylab.subplots(nrows=n_rows, ncols=n_cols)

    axes[0].set_title('Train set')
    ds['train'].iloc[:, :-1].T.plot(ax=axes[0], legend=None)

    axes[1].set_title('Validate set')
    ds['validate'].iloc[:, :-1].T.plot(ax=axes[1], legend=None)

    # actually showing the plot
    pylab.show()


def plot_mvda_archeology_train_by_quarry():
    # loading the mvda archeology data set
    ds_train = load_mvda_archeology()['train']

    # getting unique set of varieties
    y = np.unique(ds_train['Quarry'].tolist())

    # creating the figure and adding subplots
    n_rows, n_cols = 2, 2
    fig, axes = pylab.subplots(nrows=n_rows, ncols=n_cols)

    # for each variety
    for idx, label in enumerate(y):
        i, j = int(idx / n_cols), idx % n_cols
        axes[i][j].set_title(label)
        ds_train[ds_train['Quarry'] == label].iloc[:, :-2].T.plot(ax=axes[i][j], legend=None)

    # actually showing the plot
    pylab.show()
