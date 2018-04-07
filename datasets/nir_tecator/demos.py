#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, March 2017

import pylab
from datasets.nir_tecator import load_nir_tecator

# ---------------------------------------------------------------


def plot_nir_tecator_data_set():
    # loading the nir tecator data set
    ds = load_nir_tecator()

    # removing columns associated with classes and properties
    ds = ds.iloc[:, :-2]

    # plotting the data set
    ds.T.plot(legend=None)
    pylab.show()


def plot_nir_tecator_by_class():
    # loading the nir tecator data set
    ds = load_nir_tecator()

    # creating the figure and adding subplots
    fig, axes = pylab.subplots(nrows=1, ncols=2)

    # plotting class 0 samples
    axes[0].set_title('NIR Tecator (Class 0)(%fat < 20)')
    ds[ds['class'] == 0].iloc[:, :-2].T.plot(ax=axes[0], legend=None)

    # plotting class 1 samples
    axes[1].set_title('NIR Tecator (Class 1)(%fat >= 20)')
    ds[ds['class'] == 1].iloc[:, :-2].T.plot(ax=axes[1], legend=None)

    # actually showing the plot
    pylab.show()
