#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, February 2017

import pylab
from datasets.raman_porkfat import load_raman_porkfat

# ---------------------------------------------------------------


def plot_raman_porkfat_data_set():
    # loading the raman porkfat data set
    ds = load_raman_porkfat()

    # removing columns associated with classes and properties
    ds = ds.iloc[:, :-22]

    # plotting the data set
    ds.T.plot(legend=None)
    pylab.show()


def plot_raman_porkfat_props_behavior():
    # loading the raman porkfat data set
    ds = load_raman_porkfat()

    # getting the properties columns
    ds_props = ds.iloc[:, -22+3:]

    # plotting the data set
    ds_props.plot()
    pylab.show()
