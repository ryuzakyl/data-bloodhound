#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, January 2017

import pylab

from datasets.mvda_peas_raw import load_mvda_peas_raw

# ---------------------------------------------------------------


def plot_mvda_peas_raw_data_set():
    # loading the mvda peas raw data set
    ds = load_mvda_peas_raw()

    # removing columns associated with properties properties
    ds = ds.iloc[:, 3:]

    # plotting the data set
    ds.T.plot(legend=None)
    pylab.show()


def plot_mvda_peas_raw_sample1():
    # loading the mvda peas raw data set
    ds = load_mvda_peas_raw()

    sample_name = 1.0
    sample_df = None

    # removing columns associated with properties properties
    for (s_id, df) in ds.groupby('Sample #'):
        if s_id == sample_name:
            sample_df = df
            break

    sample_df = sample_df.iloc[:, 3:]

    # plotting the data set
    sample_df.T.plot()
    pylab.show()


def plot_mvda_peas_raw_properties_behavior():
    # loading the mvda peas raw data set
    ds = load_mvda_peas_raw()

    # removing sample number
    ds = ds.iloc[:, 3:]

    # plotting the data set
    ds.plot()
    pylab.show()
