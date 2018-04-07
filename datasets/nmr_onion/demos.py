#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, February 2017

import pylab
from datasets.nmr_onion import load_nmr_onion

# ---------------------------------------------------------------


def plot_nmr_onion_data_set():
    # loading the nmr onion data set
    ds = load_nmr_onion()

    # removing columns associated with classes and properties
    ds = ds.iloc[:, :-1]

    # plotting the data set
    ds.T.plot(legend=None)
    pylab.show()


def plot_nmr_onion_props_behavior():
    # loading the nmr onion data set
    ds = load_nmr_onion()

    # getting the properties columns
    ds_props = ds['% onion']

    # plotting the data set
    ds_props.T.plot(legend='top_left')
    pylab.show()
