#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, February 2017

import pylab
from datasets.nir_fuel import load_nir_fuel

# ---------------------------------------------------------------


def plot_nir_fuel_data_set():
    # loading the nir fuel data set
    ds = load_nir_fuel()

    # removing columns associated with properties properties
    ds = ds.iloc[:, :-7]

    # plotting the data set
    ds.T.plot(legend=None)
    pylab.show()


def plot_nir_fuel_properties_behavior():
    # loading the nir fuel data set
    ds = load_nir_fuel()

    # removing columns associated with properties properties
    ds = ds.iloc[:, -7:]

    # plotting the data set
    ds.plot()
    pylab.show()
