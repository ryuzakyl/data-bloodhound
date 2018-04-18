#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, January 2017

import pylab
import matplotlib.pyplot as plt

from datasets.nir_alcohol import load_nir_alcohol

# ---------------------------------------------------------------


def plot_nir_alcohol_data_sets():
    # loading the nir alcohol data set
    ds = load_nir_alcohol()

    # removing columns associated with properties
    ds = ds.iloc[:, :-3]

    # creating the figure and adding subplots
    fig, axes = plt.subplots(nrows=1, ncols=2)

    # plotting the train data
    axes[0].set_title('NIR alcohol (raw data)')
    ds.ix['train'].T.plot(ax=axes[0], legend=None)

    # plotting the MSC corrected data
    axes[1].set_title('NIR alcohol (MSC corrected)')
    ds.ix['msc'].T.plot(ax=axes[1], legend=None)

    # actually showing the plot
    pylab.show()
