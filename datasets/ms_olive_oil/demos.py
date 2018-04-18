#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, February 2017

import pylab
from datasets.ms_olive_oil import load_ms_olive_oil

# ---------------------------------------------------------------


def plot_ms_olive_oil_data_set():
    # loading the ms olive oil data set
    ds = load_ms_olive_oil()

    # excluding class labels
    ds_reduced = ds.iloc[:, :-1]

    ds_reduced.T.plot(legend=None)
    pylab.show()


def plot_ms_olive_oil_of_class_5():
    # loading the ms olive oil data set
    ds = load_ms_olive_oil()

    # getting samples of class 5
    ds_class5 = ds.loc[ds['Class'] == 5]

    # excluding class labels
    ds_class5_data = ds_class5.iloc[:, :-1]

    ds_class5_data.T.plot()
    pylab.show()
