#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, January 2017

import pylab

from datasets.mvda_alcohol import load_mvda_alcohol

# ---------------------------------------------------------------


def plot_mvda_alcohol_data_set():
    # loading the mvda alcohol data set
    ds = load_mvda_alcohol()

    # removing columns associated with properties properties
    ds = ds.iloc[:, :-1]

    # plotting the data set
    ds.T.plot(legend=None)
    pylab.show()


def plot_mvda_alcohol_properties_behavior():
    # loading the mvda alcohol data set
    ds = load_mvda_alcohol()

    # removing columns associated with properties properties
    ds = ds.iloc[:, :-1]

    # plotting the data set
    ds.plot(legend=None)
    pylab.show()
