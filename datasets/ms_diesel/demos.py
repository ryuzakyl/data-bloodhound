#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, February 2017

import pylab
from datasets.ms_diesel import load_ms_diesel

# ---------------------------------------------------------------


def plot_ms_diesel_data_set():
    # loading the ms diesel data set
    ds = load_ms_diesel()

    # excluding class labels
    ds_reduced = ds.iloc[:, :-2]

    ds_reduced.T.plot(legend=None)
    pylab.show()


def plot_ms_diesel_of_class_1():
    # loading the ms diesel data set
    ds = load_ms_diesel()

    # getting samples of class 1
    ds_class1 = ds.loc[ds['Class'] == 1]

    # excluding class labels
    ds_class1_data = ds_class1.iloc[:, :-2]

    ds_class1_data.T.plot()
    pylab.show()
