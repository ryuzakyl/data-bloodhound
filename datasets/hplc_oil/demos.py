#!/usr/bin/env
# -*- coding: utf-8 -*-
# Copyright (C) CENATAV, DATYS - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Victor M. Mendiola Lau <vmendiola@cenatav.co.cu>, February 2017

import pylab
from datasets.hplc_oil import load_hplc_oil

# ---------------------------------------------------------------


def plot_hplc_oil_data_set():
    # loading the hplc oil data set
    ds = load_hplc_oil()

    # excluding class labels
    ds_reduced = ds.iloc[:, :-2]

    ds_reduced.T.plot(legend=None)
    pylab.show()
