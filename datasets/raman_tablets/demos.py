#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, February 2017

import pylab
from datasets.raman_tablets import load_raman_tablets

# ---------------------------------------------------------------


def plot_raman_tablets_data_set():
    # loading the raman tablets data set
    ds = load_raman_tablets()

    # removing columns associated with classes and properties
    ds = ds.iloc[:, :-2]

    # plotting the data set
    ds.T.plot(legend=None)
    pylab.show()


def plot_raman_tablets_class1_subset():
    # loading the raman tablets data set
    ds = load_raman_tablets()

    # getting samples of class1
    ds_class1 = ds.loc[ds['Type'] == 1]

    # removing columns associated with classes and properties
    ds_class1 = ds_class1.iloc[:, :-2]

    # getting the subset (getting the 1/4 of the data set)
    ub_rows = int(ds_class1.shape[0] / 7)
    ds_class1 = ds_class1.iloc[:ub_rows, :]

    # plotting the data set
    ds_class1.T.plot()
    pylab.show()
