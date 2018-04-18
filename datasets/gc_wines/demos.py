#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, February 2017

import pylab
from datasets.gc_wines import load_gc_wines

# ---------------------------------------------------------------


def plot_gc_wines_data_set():
    # loading the 'gc_wines' data set
    ds = load_gc_wines()

    # excluding class labels
    ds_reduced = ds.iloc[:, :-1]

    ds_reduced.T.plot(legend=None)
    pylab.show()


def plot_gc_wines_of_origin_argentina():
    # loading the 'gc_wines' data set
    ds = load_gc_wines()

    # getting samples taken in Argentina
    ds_argentina = ds.loc[ds['origin'] == 1]

    # excluding class labels
    ds_argentina_data = ds_argentina.iloc[:, :-1]

    ds_argentina_data.T.plot()
    pylab.show()
