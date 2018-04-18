#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, February 2017

import pylab
from datasets.nir_sugarcane import load_nir_sugarcane

# ---------------------------------------------------------------


def plot_nir_sugarcane_data_set():
    # loading the nir sugarcane data set
    ds = load_nir_sugarcane()

    # removing columns associated with classes and properties
    ds = ds.iloc[:, :-5]

    # plotting the data set
    ds.T.plot(legend=None)
    pylab.show()


def plot_nir_sugarcane_juice_process():
    # loading the nir sugarcane data set
    ds = load_nir_sugarcane()

    # getting samples of juice process
    ds_juice = ds.loc[ds['Process step'] == 'juice']

    # removing columns associated with classes and properties
    ds_juice = ds_juice.iloc[:, :-5]

    # plotting the data set
    ds_juice.T.plot(legend=None)
    pylab.show()
