#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, February 2017

import pylab
from datasets.nmr_wine import load_nmr_wines

# ---------------------------------------------------------------


def plot_nmr_wine_data_set():
    # loading the nmr wine data set
    ds = load_nmr_wines()['wine_data']

    # removing columns associated with classes and properties
    ds = ds.iloc[:, :-17]

    # plotting the data set
    ds.T.plot(legend=None)
    pylab.show()


def plot_nmr_wine_props_behavior():
    # loading the nmr wine data set
    ds = load_nmr_wines()['wine_data']

    # getting the properties columns
    ds_props = ds.iloc[:, -17:]

    # plotting the data set
    ds_props.plot()
    pylab.show()
