#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) Victor M. Mendiola Lau - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <ryuzakyl@gmail.com>, February 2017

import pylab
from datasets.ms_cola import load_ms_cola

# ---------------------------------------------------------------


def plot_ms_cola_data_set():
    # loading the ms cola data set
    ds = load_ms_cola()

    # excluding class labels
    ds_reduced = ds.iloc[:, :-1]

    ds_reduced.T.plot(legend=None)
    pylab.show()
