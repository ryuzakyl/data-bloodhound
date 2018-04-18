#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, February 2017

import pylab
from datasets.ms_glycol import load_ms_glycol

# ---------------------------------------------------------------


def plot_ms_glycol1_data_set():
    # loading the ms glycol1 data set
    ds = load_ms_glycol()['glycol1']

    # excluding class labels
    ds_reduced = ds.iloc[:, :-1]

    ds_reduced.T.plot(legend=None)
    pylab.show()


def plot_ms_glycol2_data_set():
    # loading the ms glycol2 data set
    ds = load_ms_glycol()['glycol2']

    # excluding class labels
    ds_reduced = ds.iloc[:, :-1]

    ds_reduced.T.plot(legend=None)
    pylab.show()
