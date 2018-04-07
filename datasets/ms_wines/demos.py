#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, February 2017

import pylab
from datasets.ms_wines import load_ms_wines

# ---------------------------------------------------------------


def plot_ms_wines_data_set():
    # loading the 'ms_wines' data set
    ds = load_ms_wines()

    # excluding class labels
    ds_reduced = ds.iloc[:, :-1]

    ds_reduced.T.plot(legend=None)
    pylab.show()


def plot_ms_wines_of_origin_argentina():
    # loading the 'ms_wines' data set
    ds = load_ms_wines()

    # getting samples taken in Argentina
    ds_argentina = ds.loc[ds['origin'] == 1]

    # excluding class labels
    ds_argentina_data = ds_argentina.iloc[:, :-1]

    ds_argentina_data.T.plot()
    pylab.show()
